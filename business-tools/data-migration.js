/**
 * SC Pressure Point - Data Migration Script
 * Migrates combined customer/job records into separate data stores
 * Local storage with optional cloud sync
 */

const PPW_DATA = {
    CUSTOMERS_KEY: 'ppw-customers',
    JOBS_KEY: 'ppw-jobs',
    MIGRATED_KEY: 'ppw-data-migrated-v2',
    SYNC_CONFIG_KEY: 'ppw-sync-config',
    SYNC_ENABLED_KEY: 'ppw-sync-enabled',
    LAST_SYNC_KEY: 'ppw-sync-last',
    SYNC_LOG_KEY: 'ppw-sync-log',
    SYNC_STATUS_KEY: 'ppw-sync-status',
    SYNC_CLIENT_ID_KEY: 'ppw-sync-client-id',
    
    _syncTimer: null,
    _firebaseReady: null,
    _db: null,
    _ref: null,

    // Diagnostics helpers
    getClientId() {
        let id = localStorage.getItem(this.SYNC_CLIENT_ID_KEY);
        if (!id) {
            id = 'client_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6);
            localStorage.setItem(this.SYNC_CLIENT_ID_KEY, id);
        }
        return id;
    },

    logSync(event, details = '') {
        try {
            const log = JSON.parse(localStorage.getItem(this.SYNC_LOG_KEY) || '[]');
            log.unshift({
                ts: Date.now(),
                event,
                details: typeof details === 'string' ? details : JSON.stringify(details)
            });
            localStorage.setItem(this.SYNC_LOG_KEY, JSON.stringify(log.slice(0, 50)));
        } catch (e) {
            // ignore logging errors
        }
    },

    setSyncStatus(partial) {
        try {
            const current = JSON.parse(localStorage.getItem(this.SYNC_STATUS_KEY) || '{}');
            const next = { ...current, ...partial, updatedAt: Date.now() };
            localStorage.setItem(this.SYNC_STATUS_KEY, JSON.stringify(next));
        } catch (e) {
            // ignore status errors
        }
    },

    getSyncStatus() {
        try {
            return JSON.parse(localStorage.getItem(this.SYNC_STATUS_KEY) || '{}');
        } catch {
            return {};
        }
    },

    getSyncLog() {
        try {
            return JSON.parse(localStorage.getItem(this.SYNC_LOG_KEY) || '[]');
        } catch {
            return [];
        }
    },

    clearSyncLog() {
        localStorage.removeItem(this.SYNC_LOG_KEY);
    },
    
    // Get all customers
    getCustomers() {
        return JSON.parse(localStorage.getItem(this.CUSTOMERS_KEY) || '[]');
    },
    
    // Get all jobs
    getJobs() {
        return JSON.parse(localStorage.getItem(this.JOBS_KEY) || '[]');
    },
    
    // Save customers
    saveCustomers(customers) {
        localStorage.setItem(this.CUSTOMERS_KEY, JSON.stringify(customers));
        this.scheduleSync();
    },
    
    // Save jobs
    saveJobs(jobs) {
        localStorage.setItem(this.JOBS_KEY, JSON.stringify(jobs));
        this.scheduleSync();
    },
    
    // Add a customer
    addCustomer(customer) {
        const customers = this.getCustomers();
        customers.push(customer);
        this.saveCustomers(customers);
        return customer;
    },
    
    // Add a job
    addJob(job) {
        const jobs = this.getJobs();
        jobs.push(job);
        this.saveJobs(jobs);
        return job;
    },
    
    // Update a customer
    updateCustomer(id, updates) {
        const customers = this.getCustomers();
        const index = customers.findIndex(c => c.id === id);
        if (index >= 0) {
            customers[index] = { ...customers[index], ...updates, lastUpdated: new Date().toISOString() };
            this.saveCustomers(customers);
            return customers[index];
        }
        return null;
    },
    
    // Update a job
    updateJob(id, updates) {
        const jobs = this.getJobs();
        const index = jobs.findIndex(j => j.id === id);
        if (index >= 0) {
            jobs[index] = { ...jobs[index], ...updates, lastUpdated: new Date().toISOString() };
            this.saveJobs(jobs);
            return jobs[index];
        }
        return null;
    },
    
    // Delete a customer
    deleteCustomer(id) {
        const customers = this.getCustomers().filter(c => c.id !== id);
        this.saveCustomers(customers);
    },
    
    // Delete a job
    deleteJob(id) {
        const jobs = this.getJobs().filter(j => j.id !== id);
        this.saveJobs(jobs);
    },
    
    // Find customer by ID
    findCustomer(id) {
        return this.getCustomers().find(c => c.id === id);
    },
    
    // Find job by ID
    findJob(id) {
        return this.getJobs().find(j => j.id === id);
    },
    
    // Get jobs for a customer
    getJobsForCustomer(customerId) {
        return this.getJobs().filter(j => j.customerId === customerId);
    },
    
    // Find or create customer by name+phone
    findOrCreateCustomer(name, phone, email = '', address = '') {
        if (!name) return null;
        
        const customers = this.getCustomers();
        // Try to match by name+phone
        let customer = customers.find(c => 
            c.name.toLowerCase() === name.toLowerCase() && 
            (c.phone === phone || (!c.phone && !phone))
        );
        
        if (!customer) {
            customer = {
                id: 'cust_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
                name: name,
                phone: phone || '',
                email: email || '',
                address: address || '',
                notes: '',
                dateAdded: new Date().toISOString(),
                lastUpdated: new Date().toISOString()
            };
            customers.push(customer);
            this.saveCustomers(customers);
        }
        
        return customer;
    },
    
    // Run migration from old combined format
    migrate() {
        // Already migrated?
        if (localStorage.getItem(this.MIGRATED_KEY)) {
            return false;
        }
        
        const oldData = JSON.parse(localStorage.getItem(this.CUSTOMERS_KEY) || '[]');
        
        // Check if data looks like old format (has jobDate or serviceType at root level)
        const needsMigration = oldData.some(record => 
            record.jobDate || record.serviceType || record.status === 'scheduled' || record.status === 'completed'
        );
        
        if (!needsMigration || oldData.length === 0) {
            localStorage.setItem(this.MIGRATED_KEY, 'true');
            return false;
        }
        
        console.log('Running PPW data migration...');
        
        const customers = [];
        const jobs = [];
        const customerMap = new Map(); // name+phone -> customer
        
        oldData.forEach(record => {
            // Create/find customer
            const customerKey = `${record.name?.toLowerCase() || ''}_${record.phone || ''}`;
            let customer = customerMap.get(customerKey);
            
            if (!customer && record.name) {
                customer = {
                    id: 'cust_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
                    name: record.name,
                    phone: record.phone || '',
                    email: record.email || '',
                    address: record.address || '',
                    notes: '',
                    dateAdded: record.dateAdded || new Date().toISOString(),
                    lastUpdated: new Date().toISOString()
                };
                customers.push(customer);
                customerMap.set(customerKey, customer);
            }
            
            // Create job if there's job data
            const hasJobData = record.jobDate || record.serviceType || record.quoteAmount || 
                              record.status === 'scheduled' || record.status === 'completed' || record.status === 'quoted';
            
            if (hasJobData) {
                const job = {
                    id: 'job_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
                    customerId: customer?.id || null,
                    customerName: record.name || '',
                    customerPhone: record.phone || '',
                    address: record.address || '',
                    serviceType: record.serviceType || '',
                    jobDate: record.jobDate || '',
                    jobTime: record.jobTime || '',
                    jobDuration: record.jobDuration || '',
                    quoteAmount: record.quoteAmount || '',
                    squareFootage: record.squareFootage || '',
                    status: record.status || 'new',
                    notes: record.notes || '',
                    waiverSigned: record.waiverSigned || false,
                    beforePhotos: record.beforePhotos || [],
                    afterPhotos: record.afterPhotos || [],
                    googleEventId: record.googleEventId || null,
                    followUpDate: record.followUpDate || '',
                    dateAdded: record.dateAdded || new Date().toISOString(),
                    lastUpdated: new Date().toISOString()
                };
                jobs.push(job);
            }
        });
        
        // Save migrated data
        this.saveCustomers(customers);
        this.saveJobs(jobs);
        localStorage.setItem(this.MIGRATED_KEY, 'true');
        
        console.log(`Migration complete: ${customers.length} customers, ${jobs.length} jobs`);
        return true;
    },
    
    // Clear all data
    clearAll() {
        localStorage.removeItem(this.CUSTOMERS_KEY);
        localStorage.removeItem(this.JOBS_KEY);
        localStorage.removeItem(this.MIGRATED_KEY);
    },
    
    // Export all data
    exportAll() {
        return {
            version: 2,
            exportedAt: new Date().toISOString(),
            customers: this.getCustomers(),
            jobs: this.getJobs()
        };
    },
    
    // Import data
    importData(data) {
        if (data.version === 2) {
            // New format
            if (data.customers) this.saveCustomers(data.customers);
            if (data.jobs) this.saveJobs(data.jobs);
            localStorage.setItem(this.MIGRATED_KEY, 'true');
        } else {
            // Old format - save and run migration
            localStorage.removeItem(this.MIGRATED_KEY);
            this.saveCustomers(data.customers || data);
            this.migrate();
        }
    },
    
    // ===== Cloud Sync (Firebase Realtime Database) =====
    getSyncConfig() {
        try {
            return JSON.parse(localStorage.getItem(this.SYNC_CONFIG_KEY) || 'null');
        } catch {
            return null;
        }
    },
    
    setSyncConfig(config) {
        localStorage.setItem(this.SYNC_CONFIG_KEY, JSON.stringify(config));
    },
    
    isSyncEnabled() {
        return localStorage.getItem(this.SYNC_ENABLED_KEY) === 'true';
    },
    
    async enableSync() {
        localStorage.setItem(this.SYNC_ENABLED_KEY, 'true');
        const ready = await this.initCloudSync();
        if (ready) {
            await this.pushToCloud();
        }
        return ready;
    },
    
    disableSync() {
        localStorage.removeItem(this.SYNC_ENABLED_KEY);
        if (this._ref) this._ref.off();
        this._ref = null;
        this._db = null;
        this.setSyncStatus({ status: 'disabled' });
        this.logSync('disabled');
    },
    
    async initCloudSync() {
        const config = this.getSyncConfig();
        if (!config || !this.isSyncEnabled()) return false;
        if (typeof window === 'undefined') return false;

        const syncKey = (config.syncKey || '').trim();
        if (!syncKey || !config.apiKey || !config.projectId || !config.databaseURL) {
            this.logSync('init_fail', 'missing_config');
            this.setSyncStatus({ status: 'config_missing' });
            return false;
        }

        this.logSync('init_start');
        this.setSyncStatus({ status: 'init' });
        try {
            await this.loadFirebaseSDK();
        } catch (err) {
            this.logSync('sdk_error', err.message || err);
            this.setSyncStatus({ status: 'sdk_error', lastError: err.message || String(err) });
            return false;
        }
        if (!window.firebase) {
            this.logSync('sdk_missing', 'firebase_not_found');
            this.setSyncStatus({ status: 'sdk_missing' });
            return false;
        }
        
        const fbConfig = {
            apiKey: config.apiKey,
            authDomain: config.authDomain || (config.projectId ? `${config.projectId}.firebaseapp.com` : undefined),
            projectId: config.projectId,
            databaseURL: config.databaseURL
        };
        
        if (!firebase.apps.length) {
            firebase.initializeApp(fbConfig);
            this.logSync('app_init');
        }

        try {
            const auth = firebase.auth();
            if (!auth.currentUser) {
                await auth.signInAnonymously();
            }
            if (auth.currentUser) {
                this.setSyncStatus({
                    authUid: auth.currentUser.uid,
                    authIsAnonymous: !!auth.currentUser.isAnonymous
                });
                this.logSync('auth_ok', { uid: auth.currentUser.uid, anon: !!auth.currentUser.isAnonymous });
            }
        } catch (err) {
            this.logSync('auth_error', err.message || err);
            this.setSyncStatus({ status: 'auth_error', lastError: err.message || String(err) });
            return false;
        }
        this._db = firebase.database();
        this._ref = this._db.ref(`ppw-data/${syncKey}`);
        this.setSyncStatus({ status: 'ready', clientId: this.getClientId() });
        this.logSync('ref_ready', `ppw-data/${syncKey}`);
        
        this.listenForRemoteChanges();
        await this.pullFromCloud();
        return true;
    },
    
    listenForRemoteChanges() {
        if (!this._ref) return;
        this._ref.on('value', (snapshot) => {
            const data = snapshot.val();
            if (!data) return;
            const lastSync = parseInt(localStorage.getItem(this.LAST_SYNC_KEY) || '0', 10);
            const updatedAt = data.updatedAt || 0;
            if (updatedAt && updatedAt <= lastSync) return;
            
            this.importData(data);
            if (data.settings) {
                localStorage.setItem('ppw-settings', JSON.stringify(data.settings));
            }
            localStorage.setItem(this.LAST_SYNC_KEY, String(updatedAt || Date.now()));
            this.setSyncStatus({ lastRemoteUpdateAt: updatedAt || Date.now() });
            this.logSync('remote_update', { updatedAt: updatedAt || Date.now() });
        });
    },
    
    async pullFromCloud() {
        if (!this._ref) return;
        try {
            const snapshot = await this._ref.get();
            if (!snapshot.exists()) {
                this.logSync('pull_empty');
                return;
            }
            const data = snapshot.val();
            const lastSync = parseInt(localStorage.getItem(this.LAST_SYNC_KEY) || '0', 10);
            const updatedAt = data.updatedAt || 0;
            if (updatedAt && updatedAt <= lastSync) return;
            
            this.importData(data);
            if (data.settings) {
                localStorage.setItem('ppw-settings', JSON.stringify(data.settings));
            }
            localStorage.setItem(this.LAST_SYNC_KEY, String(updatedAt || Date.now()));
            this.setSyncStatus({ lastPullAt: Date.now() });
            this.logSync('pull_ok', { updatedAt: updatedAt || Date.now() });
        } catch (err) {
            this.logSync('pull_error', err.message || err);
            this.setSyncStatus({ lastError: err.message || String(err) });
        }
    },
    
    async pushToCloud() {
        if (!this.isSyncEnabled()) return;
        if (!this._ref) await this.initCloudSync();
        if (!this._ref) return;
        
        const payload = this.exportAll();
        payload.settings = JSON.parse(localStorage.getItem('ppw-settings') || '{}');
        payload.updatedAt = Date.now();
        
        try {
            await this._ref.set(payload);
            localStorage.setItem(this.LAST_SYNC_KEY, String(payload.updatedAt));
            this.setSyncStatus({ lastPushAt: Date.now(), lastError: null });
            this.logSync('push_ok', { customers: payload.customers?.length || 0, jobs: payload.jobs?.length || 0 });
        } catch (err) {
            this.logSync('push_error', err.message || err);
            this.setSyncStatus({ lastError: err.message || String(err) });
        }
    },
    
    scheduleSync() {
        if (!this.isSyncEnabled()) return;
        clearTimeout(this._syncTimer);
        this._syncTimer = setTimeout(() => this.pushToCloud(), 1200);
        this.logSync('sync_scheduled');
    },
    
    async syncNow() {
        await this.pushToCloud();
        await this.pullFromCloud();
    },

    async testCloudSync() {
        const ready = await this.initCloudSync();
        if (!ready || !this._db) {
            this.logSync('test_fail', 'init_failed');
            return { ok: false, error: 'init_failed' };
        }
        const config = this.getSyncConfig() || {};
        const syncKey = (config.syncKey || '').trim();
        if (!syncKey) {
            this.logSync('test_fail', 'missing_syncKey');
            return { ok: false, error: 'missing_syncKey' };
        }

        const clientId = this.getClientId();
        const debugRef = this._db.ref(`ppw-debug/${syncKey}/${clientId}`);
        const payload = {
            clientId,
            ts: Date.now(),
            ua: navigator.userAgent || ''
        };
        try {
            await debugRef.set(payload);
            const snap = await debugRef.get();
            const ok = snap.exists();
            this.logSync('test_ok', ok ? 'read_back' : 'no_data');
            return { ok, data: snap.val() || null };
        } catch (err) {
            this.logSync('test_error', err.message || err);
            this.setSyncStatus({ lastError: err.message || String(err) });
            return { ok: false, error: err.message || String(err) };
        }
    },
    
    loadFirebaseSDK() {
        if (this._firebaseReady) return this._firebaseReady;
        this._firebaseReady = new Promise((resolve, reject) => {
            const loadScript = (src) => new Promise((res, rej) => {
                if (document.querySelector(`script[src="${src}"]`)) return res();
                const script = document.createElement('script');
                script.src = src;
                script.onload = () => res();
                script.onerror = () => rej(new Error(`Failed to load ${src}`));
                document.head.appendChild(script);
            });
            
            loadScript('https://www.gstatic.com/firebasejs/9.22.2/firebase-app-compat.js')
                .then(() => loadScript('https://www.gstatic.com/firebasejs/9.22.2/firebase-auth-compat.js'))
                .then(() => loadScript('https://www.gstatic.com/firebasejs/9.22.2/firebase-database-compat.js'))
                .then(resolve)
                .catch(reject);
        });
        return this._firebaseReady;
    }
};

// Auto-run migration when script loads
if (typeof window !== 'undefined') {
    PPW_DATA.migrate();
    if (PPW_DATA.isSyncEnabled()) {
        PPW_DATA.initCloudSync();
    }
}
