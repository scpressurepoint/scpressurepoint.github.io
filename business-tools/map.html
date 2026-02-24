<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#020617">
    <title>Job Map - SC Pressure Point</title>
    <script src="utils.js"></script>
    <script>
        window.tailwind = {
            config: {
                theme: {
                    extend: {
                        colors: {
                            primary: '#0ea5e9',
                            dark: '#0f172a',
                            darker: '#020617',
                        }
                    }
                }
            }
        };

        function configureMapsKeyAndReload() {
            if (configureMapsKey()) {
                loadMapsScript();
            }
        }
    </script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="app.css">
    <link rel="manifest" href="manifest.json">
    <script src="data-migration.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
    <style>
        .app-content {
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        #map {
            flex: 1;
            width: 100%;
            min-height: 300px;
        }
        .glass-card {
            background: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(10px);
        }
        .job-marker {
            background: #8b5cf6;
            border: 3px solid white;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        .job-marker.today {
            background: #0ea5e9;
            animation: pulse 2s infinite;
        }
        .job-marker.completed {
            background: #10b981;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="app-header">
        <div class="app-header-inner">
            <h1>Job Map</h1>
            <button onclick="toggleList()" class="header-btn header-btn-right">
                <i class="fas fa-list"></i>
            </button>
        </div>
    </header>

    <main class="app-content">
        <!-- Filter Tabs -->
        <div class="bg-darker px-4 py-2 border-b border-slate-700">
            <div class="max-w-lg mx-auto flex gap-2">
                <button onclick="setFilter('today')" data-filter="today" class="filter-btn px-4 py-2 rounded-lg text-sm bg-primary text-white">Today</button>
                <button onclick="setFilter('week')" data-filter="week" class="filter-btn px-4 py-2 rounded-lg text-sm bg-slate-700 text-gray-300">This Week</button>
                <button onclick="setFilter('all')" data-filter="all" class="filter-btn px-4 py-2 rounded-lg text-sm bg-slate-700 text-gray-300">All Upcoming</button>
            </div>
        </div>

        <!-- Map -->
        <div id="map"></div>
    </main>

    <!-- Job List Panel (hidden by default) -->
    <div id="jobListPanel" class="fixed bottom-0 left-0 right-0 bg-slate-800 rounded-t-2xl transform translate-y-full transition-transform duration-300 z-40" style="max-height: 60vh; bottom: 70px;">
        <div class="p-4 border-b border-slate-700 flex justify-between items-center">
            <h3 class="font-bold">Jobs (<span id="jobCount">0</span>)</h3>
            <button onclick="toggleList()" class="text-gray-400">&times;</button>
        </div>
        <div id="jobListContent" class="overflow-y-auto p-4 space-y-2" style="max-height: calc(60vh - 60px);"></div>
    </div>

    <!-- Route Button -->
    <div class="fixed left-4 right-4 z-30" style="bottom: 90px;">
        <div class="max-w-lg mx-auto">
            <button onclick="openRouteInMaps()" id="routeBtn" class="w-full bg-gradient-to-r from-primary to-purple-600 text-white py-4 rounded-xl font-semibold shadow-lg hidden">
                <i class="fas fa-route mr-2"></i>
                <span id="routeBtnText">Get Directions</span>
            </button>
        </div>
    </div>

    <!-- Info Window Template (hidden) -->
    <div id="infoWindowTemplate" class="hidden">
        <div class="p-2 min-w-[200px]">
            <h4 class="font-bold text-gray-900 text-base"></h4>
            <p class="text-sm text-gray-600"></p>
            <p class="text-sm text-purple-600 font-semibold mt-1"></p>
            <div class="flex gap-2 mt-2">
                <a class="call-btn bg-green-500 text-white px-3 py-1 rounded text-sm">Call</a>
                <a class="nav-btn bg-blue-500 text-white px-3 py-1 rounded text-sm">Navigate</a>
            </div>
        </div>
    </div>

    <script>
        const MAPS_API_KEY = 'AIzaSyBNdJwNBUJ2OWXSz5aul_pRW-xhmRgtCkM';
        let map;
        let markers = [];
        let currentFilter = 'today';
        let filteredJobs = [];
        let jobs = [];
        
        function loadData() {
            jobs = PPW_DATA.getJobs();
        }

        // Custom marker icon
        const pwIcon = L.divIcon({
            html: '<div style="background:#1E90FF;color:#fff;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:16px;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.4)">💧</div>',
            className: '',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        });

        function initMap() {
            loadData();
            // Default to Columbia, SC
            map = L.map('map').setView([33.9981, -81.0637], 11);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                maxZoom: 19
            }).addTo(map);

            loadJobs();
        }

        function setFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('bg-primary', 'text-white');
                btn.classList.add('bg-slate-700', 'text-gray-300');
                if (btn.dataset.filter === filter) {
                    btn.classList.remove('bg-slate-700', 'text-gray-300');
                    btn.classList.add('bg-primary', 'text-white');
                }
            });
            loadJobs();
        }

        function loadJobs() {
            // Clear existing markers
            markers.forEach(m => map.removeLayer(m));
            markers = [];

            const today = new Date().toISOString().split('T')[0];
            const weekEnd = new Date();
            weekEnd.setDate(weekEnd.getDate() + 7);
            const weekEndStr = weekEnd.toISOString().split('T')[0];

            // Filter jobs based on current filter
            filteredJobs = jobs.filter(j => {
                if (!j.address || !j.jobDate) return false;
                if (j.status === 'completed') return false;
                
                if (currentFilter === 'today') {
                    return j.jobDate === today;
                } else if (currentFilter === 'week') {
                    return j.jobDate >= today && j.jobDate <= weekEndStr;
                } else {
                    return j.jobDate >= today;
                }
            });

            // Sort by date and time
            filteredJobs.sort((a, b) => {
                if (a.jobDate !== b.jobDate) return a.jobDate.localeCompare(b.jobDate);
                return (a.jobTime || '09:00').localeCompare(b.jobTime || '09:00');
            });

            document.getElementById('jobCount').textContent = filteredJobs.length;

            if (filteredJobs.length === 0) {
                document.getElementById('routeBtn').classList.add('hidden');
                renderJobList();
                return;
            }

            // Show route button
            document.getElementById('routeBtn').classList.remove('hidden');
            document.getElementById('routeBtnText').textContent = 
                filteredJobs.length === 1 ? 'Get Directions' : `Route ${filteredJobs.length} Jobs`;

            // Geocode addresses via Google and add Leaflet markers
            const bounds = [];
            let geocodeCount = 0;

            filteredJobs.forEach((job, index) => {
                geocodeAddress(job.address).then(coords => {
                    if (!coords) return;
                    
                    job._lat = coords.lat;
                    job._lng = coords.lng;

                    const isToday = job.jobDate === today;

                    const marker = L.marker([coords.lat, coords.lng], { icon: pwIcon })
                        .addTo(map)
                        .bindPopup(`
                            <strong>${job.customerName || job.name || 'Job'}</strong><br>
                            ${job.address}<br>
                            <em>${job.status || 'Scheduled'}</em><br>
                            ${job.jobDate ? new Date(job.jobDate + 'T12:00:00').toLocaleDateString() : ''}
                            ${isToday ? '<br><span style="color:#10B981;font-weight:bold">● Today</span>' : ''}
                            ${job.quoteAmount ? `<br><strong style="color:#10b981">$${job.quoteAmount}</strong>` : ''}
                            <br>
                            ${job.customerPhone ? `<a href="tel:${job.customerPhone}" style="color:#10b981">📞 Call</a> ` : ''}
                            <a href="https://maps.google.com/maps?daddr=${encodeURIComponent(job.address)}" target="_blank" style="color:#3b82f6">🚗 Navigate</a>
                        `);

                    markers.push(marker);
                    bounds.push([coords.lat, coords.lng]);

                    // Fit bounds when we have markers
                    geocodeCount++;
                    if (geocodeCount === filteredJobs.length || bounds.length > 0) {
                        if (bounds.length === 1) {
                            map.setView(bounds[0], 14);
                        } else if (bounds.length > 1) {
                            map.fitBounds(bounds, { padding: [30, 30] });
                        }
                    }
                }).catch(err => console.warn('Geocode failed for:', job.address, err));
            });

            renderJobList();
        }

        function renderJobList() {
            const container = document.getElementById('jobListContent');
            
            if (filteredJobs.length === 0) {
                container.innerHTML = `
                    <div class="text-center text-gray-400 py-8">
                        <i class="fas fa-map-marker-alt text-3xl mb-2"></i>
                        <p>No jobs with addresses for this period</p>
                    </div>
                `;
                return;
            }

            const today = new Date().toISOString().split('T')[0];

            container.innerHTML = filteredJobs.map((job, i) => {
                const isToday = job.jobDate === today;
                const dateStr = new Date(job.jobDate + 'T12:00:00').toLocaleDateString('en-US', { 
                    weekday: 'short', month: 'short', day: 'numeric' 
                });

                return `
                    <div class="bg-slate-700 rounded-xl p-3 flex items-center gap-3" onclick="focusJob(${i})">
                        <div class="w-8 h-8 rounded-full ${isToday ? 'bg-primary' : 'bg-purple-600'} flex items-center justify-center text-white font-bold">
                            ${i + 1}
                        </div>
                        <div class="flex-1">
                            <p class="font-semibold">${job.customerName || job.name || 'Job'}</p>
                            <p class="text-sm ${isToday ? 'text-primary' : 'text-purple-400'}">${isToday ? 'TODAY' : dateStr} ${job.jobTime || ''}</p>
                        </div>
                        ${job.quoteAmount ? `<span class="text-green-400 font-bold">$${job.quoteAmount}</span>` : ''}
                    </div>
                `;
            }).join('');
        }

        function focusJob(index) {
            const job = filteredJobs[index];
            if (job._lat && job._lng) {
                map.setView([job._lat, job._lng], 15);
                if (markers[index]) markers[index].openPopup();
            }
            toggleList();
        }

        function toggleList() {
            const panel = document.getElementById('jobListPanel');
            panel.classList.toggle('translate-y-full');
        }

        function openRouteInMaps() {
            if (filteredJobs.length === 0) return;
            const jobsWithCoords = filteredJobs.filter(j => j.address);
            if (jobsWithCoords.length === 1) {
                window.open(`https://maps.google.com/maps?daddr=${encodeURIComponent(jobsWithCoords[0].address)}`, '_blank');
            } else {
                const waypoints = jobsWithCoords.map(j => encodeURIComponent(j.address)).join('/');
                window.open(`https://www.google.com/maps/dir/${waypoints}`, '_blank');
            }
        }

        // Google Geocoding helper
        function geocodeAddress(address) {
            return fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(address)}&key=${MAPS_API_KEY}`)
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'OK' && data.results[0]) {
                        const loc = data.results[0].geometry.location;
                        return { lat: loc.lat, lng: loc.lng };
                    }
                    return null;
                });
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            initMap();
            setActiveNav();
        });

        // Refresh on visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                loadData();
                if (map) loadJobs();
            }
        });
    </script>

    <!-- Bottom Tab Bar -->
    <nav class="tab-bar">
        <div class="tab-bar-inner">
            <a href="index.html" class="tab-item">
                <i class="fas fa-home"></i>
                <span>Home</span>
            </a>
            <a href="jobs.html" class="tab-item">
                <i class="fas fa-briefcase"></i>
                <span>Jobs</span>
            </a>
            <a href="quick-add.html" class="tab-item tab-item-add">
                <div class="tab-add-btn">
                    <i class="fas fa-plus"></i>
                </div>
                <span>Add</span>
            </a>
            <a href="calendar.html" class="tab-item">
                <i class="fas fa-calendar"></i>
                <span>Calendar</span>
            </a>
            <a href="customer-tracker.html" class="tab-item">
                <i class="fas fa-users"></i>
                <span>Customers</span>
            </a>
        </div>
    </nav>
</body>
</html>
