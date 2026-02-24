/**
 * SC Pressure Point - Firebase Auth & Sync Module
 * 
 * This module handles:
 * - User authentication (Google sign-in)
 * - Cloud data sync via Firestore
 * - Offline-first with sync when online
 * 
 * Just sign in with Google and your data syncs automatically!
 */

const PPW_FIREBASE = (function() {
    let app = null;
    let auth = null;
    let db = null;
    let currentUser = null;
    let isInitialized = false;
    let syncInProgress = false;

    // Hardcoded Firebase config - no setup needed!
    const FIREBASE_CONFIG = {
        apiKey: "AIzaSyDtiQgexvwyBni2uakvbFnX7ZWS11ribSs",
        authDomain: "scpressurepoint-245d4.firebaseapp.com",
        databaseURL: "https://scpressurepoint-245d4-default-rtdb.firebaseio.com",
        projectId: "scpressurepoint-245d4",
        storageBucket: "scpressurepoint-245d4.firebasestorage.app",
        messagingSenderId: "931285544673",
        appId: "1:931285544673:web:793a89965e4552829191a0",
        measurementId: "G-0SQF35D9JY"
    };

    // Get Firebase config (hardcoded)
    function getConfig() {
        return FIREBASE_CONFIG;
    }

    // Check if Firebase is configured (always true now)
    function isConfigured() {
        return true;
    }

    // Initialize Firebase
    async function init() {
        if (isInitialized) return true;
        
        const config = getConfig();
        if (!config) {
            console.log('Firebase not configured');
            return false;
        }

        try {
            // Dynamically load Firebase SDK
            if (typeof firebase === 'undefined') {
                await loadFirebaseSDK();
            }

            // Initialize app
            if (!firebase.apps.length) {
                app = firebase.initializeApp(config);
            } else {
                app = firebase.apps[0];
            }

            auth = firebase.auth();
            db = firebase.firestore();

            // Enable offline persistence
            try {
                await db.enablePersistence({ synchronizeTabs: true });
            } catch (err) {
                console.log('Persistence already enabled or not available');
            }

            // Listen for auth state changes
            auth.onAuthStateChanged(handleAuthStateChange);

            isInitialized = true;
            console.log('Firebase initialized');
            return true;
        } catch (err) {
            console.error('Firebase init error:', err);
            return false;
        }
    }

    // Load Firebase SDK dynamically
    function loadFirebaseSDK() {
        return new Promise((resolve, reject) => {
            const scripts = [
                'https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js',
                'https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js',
                'https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js'
            ];

            let loaded = 0;
            scripts.forEach(src => {
                if (document.querySelector(`script[src="${src}"]`)) {
                    loaded++;
                    if (loaded === scripts.length) resolve();
                    return;
                }
                const script = document.createElement('script');
                script.src = src;
                script.onload = () => {
                    loaded++;
                    if (loaded === scripts.length) resolve();
                };
                script.onerror = reject;
                document.head.appendChild(script);
            });
        });
    }

    // Handle auth state changes
    function handleAuthStateChange(user) {
        currentUser = user;
        
        // Dispatch event for UI updates
        window.dispatchEvent(new CustomEvent('ppw-auth-change', { 
            detail: { user: user ? getUserInfo() : null }
        }));

        if (user) {
            console.log('User signed in:', user.email);
            // Trigger sync when user signs in
            syncFromCloud();
        } else {
            console.log('User signed out');
        }
    }

    // Get current user info
    function getUserInfo() {
        if (!currentUser) return null;
        return {
            uid: currentUser.uid,
            email: currentUser.email,
            displayName: currentUser.displayName,
            photoURL: currentUser.photoURL
        };
    }

    // Sign in with Google
    async function signInWithGoogle() {
        if (!isInitialized) {
            const ready = await init();
            if (!ready) {
                alert('Could not connect to sync service. Please try again.');
                return null;
            }
        }

        try {
            const provider = new firebase.auth.GoogleAuthProvider();
            const result = await auth.signInWithPopup(provider);
            return getUserInfo();
        } catch (err) {
            console.error('Sign-in error:', err);
            if (err.code === 'auth/popup-blocked') {
                alert('Popup was blocked. Please allow popups for this site.');
            } else if (err.code === 'auth/popup-closed-by-user') {
                // User closed the popup, no alert needed
                return null;
            } else if (err.code === 'auth/unauthorized-domain') {
                alert('This domain is not authorized for sign-in yet.');
            } else {
                alert('Sign-in failed. Please try again.');
            }
            return null;
        }
    }

    // Sign out
    async function signOut() {
        if (auth) {
            await auth.signOut();
        }
        currentUser = null;
    }

    // Sync data to cloud
    async function syncToCloud() {
        if (!currentUser || !db || syncInProgress) return false;

        syncInProgress = true;
        try {
            const userDoc = db.collection('users').doc(currentUser.uid);
            
            // Get local data
            const localData = PPW_DATA.exportAll();
            localData.lastSync = new Date().toISOString();
            localData.deviceId = getDeviceId();

            // Save to Firestore
            await userDoc.set({
                customers: localData.customers || [],
                jobs: localData.jobs || [],
                settings: JSON.parse(localStorage.getItem('ppw-settings') || '{}'),
                lastSync: firebase.firestore.FieldValue.serverTimestamp(),
                lastDevice: getDeviceId()
            }, { merge: true });

            console.log('Data synced to cloud');
            showSyncToast('Data synced to cloud');
            return true;
        } catch (err) {
            console.error('Sync to cloud failed:', err);
            return false;
        } finally {
            syncInProgress = false;
        }
    }

    // Sync data from cloud
    async function syncFromCloud() {
        if (!currentUser || !db || syncInProgress) return false;

        syncInProgress = true;
        try {
            const userDoc = await db.collection('users').doc(currentUser.uid).get();
            
            if (!userDoc.exists) {
                // First time user - upload local data
                console.log('New user - uploading local data');
                await syncToCloud();
                return true;
            }

            const cloudData = userDoc.data();
            const localData = PPW_DATA.exportAll();

            // Simple conflict resolution: cloud wins if newer
            // In production, you'd want smarter merging
            const cloudTime = cloudData.lastSync?.toDate?.() || new Date(0);
            const localTime = new Date(localStorage.getItem('ppw-last-sync') || 0);

            if (cloudTime > localTime) {
                // Cloud is newer - import it
                PPW_DATA.importData({
                    customers: cloudData.customers || [],
                    jobs: cloudData.jobs || []
                });

                if (cloudData.settings) {
                    const currentSettings = JSON.parse(localStorage.getItem('ppw-settings') || '{}');
                    // Preserve local-only settings
                    cloudData.settings.firebaseConfig = currentSettings.firebaseConfig;
                    cloudData.settings.gcalClientId = currentSettings.gcalClientId;
                    localStorage.setItem('ppw-settings', JSON.stringify(cloudData.settings));
                }

                localStorage.setItem('ppw-last-sync', new Date().toISOString());
                console.log('Data synced from cloud');
                showSyncToast('Data synced from cloud');
                
                // Notify UI to refresh
                window.dispatchEvent(new CustomEvent('ppw-sync-updated'));
            } else {
                console.log('Local data is current');
            }

            return true;
        } catch (err) {
            console.error('Sync from cloud failed:', err);
            return false;
        } finally {
            syncInProgress = false;
        }
    }

    // Get unique device ID
    function getDeviceId() {
        let deviceId = localStorage.getItem('ppw-device-id');
        if (!deviceId) {
            deviceId = 'device_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('ppw-device-id', deviceId);
        }
        return deviceId;
    }

    // Show sync toast notification
    function showSyncToast(message) {
        if (typeof showToast === 'function') {
            showToast(message);
        }
    }

    // Listen for online/offline
    window.addEventListener('online', () => {
        if (currentUser) {
            syncToCloud();
        }
    });

    // Auto-sync periodically when signed in
    setInterval(() => {
        if (currentUser && navigator.onLine) {
            syncToCloud();
        }
    }, 5 * 60 * 1000); // Every 5 minutes

    // Public API
    return {
        init,
        isConfigured,
        signInWithGoogle,
        signOut,
        getUserInfo,
        syncToCloud,
        syncFromCloud,
        get isSignedIn() { return !!currentUser; },
        get user() { return getUserInfo(); }
    };
})();

// Auto-initialize if configured
document.addEventListener('DOMContentLoaded', () => {
    if (PPW_FIREBASE.isConfigured()) {
        PPW_FIREBASE.init();
    }
});
