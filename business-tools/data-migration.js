/**
 * SC Pressure Point - Data Migration Script
 * Migrates combined customer/job records into separate data stores
 * Simple local storage with export/import
 */

const PPW_DATA = {
    CUSTOMERS_KEY: 'ppw-customers',
    JOBS_KEY: 'ppw-jobs',
    MIGRATED_KEY: 'ppw-data-migrated-v2',
    
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
    },
    
    // Save jobs
    saveJobs(jobs) {
        localStorage.setItem(this.JOBS_KEY, JSON.stringify(jobs));
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
    }
};

// Auto-run migration when script loads
if (typeof window !== 'undefined') {
    PPW_DATA.migrate();
}
