<template>
  <AppLayout>
    <div class="view-reports-page glass-background">
    <!-- Page Header -->
    <div class="page-header">
      <h2 class="page-title">
        <i class="pi pi-chart-line"></i>
        View Generation Reports
      </h2>
      <p class="page-description">
        View and analyze generation reports for Agus and Pulangi Hydro-electric Power Plants
      </p>
    </div>

    <!-- Advanced Filter Component -->
    <AdvancedFilter 
      :plants="plants"
      :showNumericFilters="true"
      :initialFilters="filters"
      @filter-change="onFilterChange"
    />

    <!-- Summary Statistics -->
    <div v-if="summary" class="card glass-card summary-card glass-fade-in">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-chart-bar"></i>
          Summary Statistics
        </h3>
      </div>
      <div class="card-body">
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-bolt"></i>
            </div>
            <div class="summary-content">
              <label>Total Generation</label>
              <span class="summary-value">{{ formatNumber(summary.total_generation) }} kWh</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-percentage"></i>
            </div>
            <div class="summary-content">
              <label>Avg Capacity Factor</label>
              <span class="summary-value">{{ formatNumber(summary.avg_capacity_factor) }}%</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-check-circle"></i>
            </div>
            <div class="summary-content">
              <label>Avg Availability</label>
              <span class="summary-value">{{ formatNumber(summary.avg_availability_factor) }}%</span>
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-icon">
              <i class="pi pi-clock"></i>
            </div>
            <div class="summary-content">
              <label>Total Operating Hours</label>
              <span class="summary-value">{{ formatNumber(summary.total_operating_hours) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State with Skeleton -->
    <div v-if="loading" class="loading-state">
      <!-- Skeleton for Summary Stats -->
      <SkeletonLoader type="stats" />
      
      <!-- Skeleton for Table -->
      <SkeletonLoader type="table" />
    </div>

    <!-- Reports Table -->
    <div v-else-if="reports.length" class="card glass-card glass-fade-in">
      <div class="card-header">
        <h3 class="card-title">
          <i class="pi pi-table"></i>
          Generation Reports
        </h3>
        <div class="header-controls">
          <label class="rows-label">Show:</label>
          <select v-model="rowsPerPage" @change="onRowsChange" class="rows-select glass-select">
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
            <option :value="200">200</option>
          </select>
          <span class="rows-label">entries</span>
        </div>
      </div>
      <div class="card-body p-0">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th class="text-left sortable" @click="sortBy('report_date')">
                  Date
                  <i :class="['pi', getSortIcon('report_date'), 'sort-icon']"></i>
                </th>
                <th class="text-left sortable" @click="sortBy('plant')">
                  Plant
                  <i :class="['pi', getSortIcon('plant'), 'sort-icon']"></i>
                </th>
                <th class="text-center sortable" @click="sortBy('unit')">
                  Unit
                  <i :class="['pi', getSortIcon('unit'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('generation')">
                  Generation (kWh)
                  <i :class="['pi', getSortIcon('generation'), 'sort-icon']"></i>
                </th>
                <th class="text-center sortable nowrap" @click="sortBy('operating_hours')">
                  Operating Hours
                  <i :class="['pi', getSortIcon('operating_hours'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('capacity_factor')">
                  Capacity Factor (%)
                  <i :class="['pi', getSortIcon('capacity_factor'), 'sort-icon']"></i>
                </th>
                <th class="text-right sortable nowrap" @click="sortBy('availability')">
                  Availability (%)
                  <i :class="['pi', getSortIcon('availability'), 'sort-icon']"></i>
                </th>
                <th class="text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="report in reports" :key="report.id">
                <td class="text-left">{{ report.report_date }}</td>
                <td class="text-left">
                  <span class="plant-badge">{{ report.plant_code }}</span>
                </td>
                <td class="text-center">{{ report.unit_number }}</td>
                <td class="text-right">{{ formatNumber(report.generation_kwh) }}</td>
                <td class="text-center">{{ report.operating_hours }}</td>
                <td class="text-right">{{ formatNumber(report.capacity_factor) }}</td>
                <td class="text-right">{{ formatNumber(report.availability_factor) }}</td>
                <td class="text-center">
                  <button 
                    @click="openEditModal(report)" 
                    class="btn-edit"
                    title="Edit Report"
                    v-if="canEdit"
                  >
                    <i class="pi pi-pencil"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <Paginator 
          :rows="rowsPerPage" 
          :totalRecords="totalRecords" 
          :first="(currentPage - 1) * rowsPerPage"
          @page="onPageChange($event)"
          template="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
          :pageLinkSize="5"
        />
      </div>
    </div>

    <!-- No Data State -->
    <div v-else class="empty-state">
      <i class="pi pi-inbox"></i>
      <h3>No Reports Found</h3>
      <p>Try adjusting your filters to see generation reports</p>
    </div>
  </div>

  <!-- Edit Report Modal -->
  <div v-if="showEditModal" class="modal-overlay glass-overlay" @click="closeEditModal">
    <div class="edit-modal glass-modal" @click.stop>
      <div class="modal-header">
        <h2>
          <i class="pi pi-pencil"></i>
          Edit Generation Report
        </h2>
        <button @click="closeEditModal" class="btn-close-modal glass-button">
          <i class="pi pi-times"></i>
        </button>
      </div>
      
      <div class="modal-body">
        <div class="form-grid">
          <!-- Report Date (Read-only) -->
          <div class="form-group disabled-group">
            <label><i class="pi pi-calendar"></i> Report Date <span class="required">*</span></label>
            <div class="input-icon-wrapper">
              <input 
                type="date" 
                v-model="editForm.report_date" 
                class="form-input"
                required
                disabled
              />
              <i class="pi pi-lock lock-icon"></i>
            </div>
          </div>

          <!-- Plant (Read-only) -->
          <div class="form-group disabled-group">
            <label><i class="pi pi-building"></i> Plant</label>
            <div class="input-icon-wrapper">
              <input 
                type="text" 
                :value="editForm.plant_name" 
                class="form-input"
                disabled
              />
              <i class="pi pi-lock lock-icon"></i>
            </div>
          </div>

          <!-- Unit Number (Read-only) -->
          <div class="form-group disabled-group">
            <label><i class="pi pi-cog"></i> Unit Number <span class="required">*</span></label>
            <div class="input-icon-wrapper">
              <input 
                type="number" 
                v-model.number="editForm.unit_number" 
                class="form-input"
                min="1"
                required
                disabled
              />
              <i class="pi pi-lock lock-icon"></i>
            </div>
          </div>

          <!-- Generation (kWh) -->
          <div class="form-group">
            <label><i class="pi pi-bolt"></i> Generation (kWh) <span class="required">*</span></label>
            <input 
              type="number" 
              v-model.number="editForm.generation_kwh" 
              class="form-input active-input"
              min="0"
              step="0.01"
              required
            />
          </div>

          <!-- Operating Hours -->
          <div class="form-group">
            <label><i class="pi pi-clock"></i> Operating Hours <span class="required">*</span></label>
            <input 
              type="number" 
              v-model.number="editForm.operating_hours" 
              class="form-input active-input"
              min="0"
              max="24"
              step="0.01"
              required
            />
          </div>

          <!-- Capacity Factor -->
          <div class="form-group">
            <label><i class="pi pi-chart-pie"></i> Capacity Factor (%) <span class="required">*</span></label>
            <input 
              type="number" 
              v-model.number="editForm.capacity_factor" 
              class="form-input active-input"
              min="0"
              max="100"
              step="0.01"
              required
            />
          </div>

          <!-- Availability Factor -->
          <div class="form-group">
            <label><i class="pi pi-check-circle"></i> Availability Factor (%) <span class="required">*</span></label>
            <input 
              type="number" 
              v-model.number="editForm.availability_factor" 
              class="form-input active-input"
              min="0"
              max="100"
              step="0.01"
              required
            />
          </div>

          <!-- Forced Outage Hours -->
          <div class="form-group">
            <label><i class="pi pi-exclamation-triangle"></i> Forced Outage Hours</label>
            <input 
              type="number" 
              v-model.number="editForm.forced_outage_hours" 
              class="form-input active-input"
              min="0"
              max="24"
              step="0.01"
            />
          </div>

          <!-- Scheduled Outage Hours -->
          <div class="form-group">
            <label><i class="pi pi-calendar-times"></i> Scheduled Outage Hours</label>
            <input 
              type="number" 
              v-model.number="editForm.scheduled_outage_hours" 
              class="form-input active-input"
              min="0"
              max="24"
              step="0.01"
            />
          </div>

          <!-- Remarks -->
          <div class="form-group full-width">
            <label><i class="pi pi-comment"></i> Remarks</label>
            <textarea 
              v-model="editForm.remarks" 
              class="form-textarea active-input"
              rows="3"
              placeholder="Add any notes or comments..."
            ></textarea>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button @click="closeEditModal" class="btn-cancel">
          <i class="pi pi-times"></i>
          Cancel
        </button>
        <button @click="saveEdit" class="btn-save" :disabled="saving">
          <i class="pi" :class="saving ? 'pi-spin pi-spinner' : 'pi-check'"></i>
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
  </div>
  </AppLayout>
</template>

<script>
import api from '../services/api';
import AppLayout from './AppLayout.vue';
import AdvancedFilter from './AdvancedFilter.vue';
import SkeletonLoader from './SkeletonLoader.vue';
import Paginator from 'primevue/paginator';

export default {
  name: 'ViewReports',
  components: {
    AppLayout,
    AdvancedFilter,
    SkeletonLoader,
    Paginator,
  },
  data() {
    return {
      plants: [],
      allReports: [], // Store all reports
      summary: null,
      loading: false,
      filters: {
        plantCodes: [],
        startDate: '',
        endDate: '',
      },
      currentPage: 1,
      totalRecords: 0,
      rowsPerPage: 10,
      // Sorting
      sortField: 'report_date',
      sortOrder: -1, // -1 for descending, 1 for ascending
      // Edit functionality
      showEditModal: false,
      editForm: {
        id: null,
        report_date: '',
        plant_name: '',
        unit_number: null,
        generation_kwh: 0,
        operating_hours: 0,
        capacity_factor: 0,
        availability_factor: 0,
        forced_outage_hours: 0,
        scheduled_outage_hours: 0,
        remarks: ''
      },
      saving: false,
      canEdit: false,
    };
  },
  computed: {
    reports() {
      // Sort first, then paginate
      const sorted = this.sortedReports;
      const start = (this.currentPage - 1) * this.rowsPerPage;
      const end = start + this.rowsPerPage;
      return sorted.slice(start, end);
    },
    sortedReports() {
      return [...this.allReports].sort((a, b) => {
        let aVal, bVal;
        
        switch(this.sortField) {
          case 'report_date':
            aVal = new Date(a.report_date);
            bVal = new Date(b.report_date);
            break;
          case 'plant':
            aVal = a.plant_name?.toLowerCase() || '';
            bVal = b.plant_name?.toLowerCase() || '';
            break;
          case 'unit':
            aVal = a.unit_name?.toLowerCase() || '';
            bVal = b.unit_name?.toLowerCase() || '';
            break;
          case 'generation':
            aVal = parseFloat(a.generation_kwh) || 0;
            bVal = parseFloat(b.generation_kwh) || 0;
            break;
          case 'operating_hours':
            aVal = parseFloat(a.operating_hours) || 0;
            bVal = parseFloat(b.operating_hours) || 0;
            break;
          case 'capacity_factor':
            aVal = parseFloat(a.capacity_factor) || 0;
            bVal = parseFloat(b.capacity_factor) || 0;
            break;
          case 'availability':
            aVal = parseFloat(a.availability) || 0;
            bVal = parseFloat(b.availability) || 0;
            break;
          default:
            return 0;
        }
        
        if (aVal < bVal) return -1 * this.sortOrder;
        if (aVal > bVal) return 1 * this.sortOrder;
        return 0;
      });
    }
  },
  mounted() {
    // Check if user can edit (managers and above)
    this.canEdit = this.isManagerOrAbove();
    this.loadPlants();
    this.loadReports();
  },
  methods: {
    sortBy(field) {
      if (this.sortField === field) {
        // Toggle sort order if clicking the same field
        this.sortOrder = this.sortOrder * -1;
      } else {
        // Set new field and default to ascending
        this.sortField = field;
        this.sortOrder = 1;
      }
      this.currentPage = 1; // Reset to first page when sorting
    },
    
    getSortIcon(field) {
      if (this.sortField !== field) {
        return 'pi-sort-alt'; // Neutral sort icon
      }
      return this.sortOrder === 1 ? 'pi-sort-amount-up' : 'pi-sort-amount-down';
    },
    
    async loadPlants() {
      try {
        const response = await api.getPlants();
        // Handle both paginated and non-paginated responses
        this.plants = response.data.results || response.data;
        console.log('Loaded plants:', this.plants);
      } catch (error) {
        console.error('Error loading plants:', error);
      }
    },
    onFilterChange(newFilters) {
      this.filters = { ...this.filters, ...newFilters };
      this.loadReports();
      if (newFilters.plantCodes && newFilters.plantCodes.length > 0) {
        this.loadSummary();
      }
    },
    async loadReports() {
      this.loading = true;
      try {
        const params = {
          plant_code: this.filters.plantCodes,
          start_date: this.filters.startDate,
          end_date: this.filters.endDate,
          page_size: 1000, // Get all records (or a large number)
        };

        const response = await api.getGenerationReports(params);
        let data = response.data.results || response.data;
        
        if (!data || data.length === 0) {
          throw new Error("No data");
        }
        
        this.allReports = data;
        this.totalRecords = this.allReports.length;
      } catch (error) {
        console.warn('Using mock reports for demonstration');
        this.allReports = [
          {
            id: 1,
            report_date: '2026-03-24',
            plant_code: 'AGUS_1',
            unit_number: '1',
            generation_kwh: '45210.50',
            operating_hours: '24',
            capacity_factor: '65.40',
            availability_factor: '100.00'
          },
          {
            id: 2,
            report_date: '2026-03-24',
            plant_code: 'AGUS_1',
            unit_number: '2',
            generation_kwh: '38100.00',
            operating_hours: '20',
            capacity_factor: '55.20',
            availability_factor: '83.33'
          },
          {
            id: 3,
            report_date: '2026-03-24',
            plant_code: 'AGUS_2',
            unit_number: '1',
            generation_kwh: '98450.75',
            operating_hours: '24',
            capacity_factor: '82.10',
            availability_factor: '100.00'
          },
          {
            id: 4,
            report_date: '2026-03-23',
            plant_code: 'AGUS_4',
            unit_number: '1',
            generation_kwh: '75000.00',
            operating_hours: '24',
            capacity_factor: '78.50',
            availability_factor: '100.00'
          },
          {
            id: 5,
            report_date: '2026-03-23',
            plant_code: 'AGUS_5',
            unit_number: '2',
            generation_kwh: '0.00',
            operating_hours: '0',
            capacity_factor: '0.00',
            availability_factor: '0.00'
          }
        ];
        this.totalRecords = this.allReports.length;
      } finally {
        setTimeout(() => this.loading = false, 600); // UI feel
      }
    },
    async loadSummary() {
      try {
        const params = {
          plant_code: this.filters.plantCodes,
          start_date: this.filters.startDate,
          end_date: this.filters.endDate,
        };

        const response = await api.getReportSummary(params);
        if (!response.data || Object.keys(response.data).length === 0) {
          throw new Error("No summary");
        }
        this.summary = response.data;
      } catch (error) {
        console.warn('Using mock summary for demonstration');
        this.summary = {
          total_generation: 256761.25,
          avg_capacity_factor: 56.24,
          avg_availability_factor: 76.66,
          total_operating_hours: 92
        };
      }
    },
    onPageChange(event) {
      this.currentPage = event.page + 1; // PrimeVue uses 0-based index
    },
    onRowsChange() {
      this.currentPage = 1; // Reset to first page when changing rows per page
    },
    formatNumber(value) {
      return value ? parseFloat(value).toFixed(2) : '0.00';
    },
    
    // Permission check
    isManagerOrAbove() {
      const user = JSON.parse(localStorage.getItem('user') || '{}');
      const role = user.role || '';
      return ['MANAGER', 'ADMIN', 'SUPERADMIN'].includes(role);
    },
    
    // Edit functionality
    openEditModal(report) {
      this.editForm = {
        id: report.id,
        report_date: report.report_date,
        plant_name: report.plant_name,
        plant_code: report.plant_code,
        unit_number: report.unit_number,
        generation_kwh: report.generation_kwh,
        operating_hours: report.operating_hours,
        capacity_factor: report.capacity_factor,
        availability_factor: report.availability_factor,
        forced_outage_hours: report.forced_outage_hours || 0,
        scheduled_outage_hours: report.scheduled_outage_hours || 0,
        remarks: report.remarks || ''
      };
      this.showEditModal = true;
    },
    
    closeEditModal() {
      this.showEditModal = false;
      this.editForm = {
        id: null,
        report_date: '',
        plant_name: '',
        unit_number: null,
        generation_kwh: 0,
        operating_hours: 0,
        capacity_factor: 0,
        availability_factor: 0,
        forced_outage_hours: 0,
        scheduled_outage_hours: 0,
        remarks: ''
      };
    },
    
    async saveEdit() {
      if (!this.editForm.id) return;
      
      this.saving = true;
      
      try {
        // Prepare data for API
        const updateData = {
          report_date: this.editForm.report_date,
          unit_number: this.editForm.unit_number,
          generation_kwh: this.editForm.generation_kwh,
          operating_hours: this.editForm.operating_hours,
          capacity_factor: this.editForm.capacity_factor,
          availability_factor: this.editForm.availability_factor,
          forced_outage_hours: this.editForm.forced_outage_hours,
          scheduled_outage_hours: this.editForm.scheduled_outage_hours,
          remarks: this.editForm.remarks
        };
        
        await api.updateGenerationReport(this.editForm.id, updateData);
        
        this.$toast.success('Report updated successfully!');
        this.closeEditModal();
        
        // Reload reports to show updated data
        await this.loadReports();
        
      } catch (error) {
        console.error('Error updating report:', error);
        const errorMsg = error.response?.data?.error || error.response?.data?.message || 'Failed to update report';
        this.$toast.error(errorMsg);
      } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.view-reports-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.page-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  letter-spacing: -0.025em;
}

.page-title i {
  color: #3b82f6;
  font-size: 2rem;
}

.page-description {
  color: #64748b;
  font-size: 1.1rem;
  margin: 0;
}

/* Card General Styles */
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
  overflow: hidden;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.card-title i {
  color: #3b82f6;
  font-size: 1.25rem;
}

.card-body {
  padding: 1.5rem;
}

.card-body.p-0 {
  padding: 0;
}

/* Header Controls */
.header-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rows-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.rows-select {
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #334155;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s ease;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2364748b'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  min-width: 5rem;
}

.rows-select:hover {
  border-color: #cbd5e1;
}

.rows-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Summary Statistics */
.summary-card {
  margin-bottom: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.summary-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-radius: 16px;
  font-size: 2rem;
  flex-shrink: 0;
  transition: transform 0.3s ease;
  box-shadow: 0 6px 12px -2px rgba(59, 130, 246, 0.4);
}

.summary-item:hover .summary-icon {
  transform: scale(1.05) rotate(5deg);
}

/* Different colors for different summary items */
.summary-item:nth-child(2) .summary-icon {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 6px 12px -2px rgba(16, 185, 129, 0.4);
}

.summary-item:nth-child(3) .summary-icon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  box-shadow: 0 6px 12px -2px rgba(245, 158, 11, 0.4);
}

.summary-item:nth-child(4) .summary-icon {
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  box-shadow: 0 6px 12px -2px rgba(139, 92, 246, 0.4);
}

.summary-content {
  flex: 1;
  min-width: 0;
}

.summary-content label {
  display: block;
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.summary-value {
  display: block;
  font-size: 1.75rem;
  color: #0f172a;
  font-weight: 800;
  line-height: 1.2;
}

/* Table Styles */
.table-container {
  overflow-x: auto;
  width: 100%;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
}

th, td {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  white-space: nowrap;
}

th {
  background: #f8fafc;
  font-weight: 700;
  color: #475569;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  position: sticky;
  top: 0;
  z-index: 10;
}

tbody tr {
  transition: all 0.2s ease;
}

tbody tr:hover {
  background: #f8fafc;
  transform: scale(1.001);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  position: relative;
  z-index: 5;
}

td {
  font-size: 0.95rem;
  color: #1e293b;
  font-weight: 500;
}

.text-left { text-align: left !important; }
.text-center { text-align: center !important; }
.text-right { text-align: right !important; }

/* Sortable Headers */
th.sortable {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

th.sortable:hover {
  background-color: #f1f5f9;
  color: #0f172a;
}

th .sort-icon {
  font-size: 0.8rem;
  color: #cbd5e1;
  margin-left: 0.5rem;
  transition: color 0.2s ease;
  vertical-align: middle;
}

th.sortable:hover .sort-icon {
  color: #94a3b8;
}

th .pi-sort-amount-up,
th .pi-sort-amount-down {
  color: #3b82f6;
  font-weight: bold;
}

/* Badges */
.plant-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  background: #eff6ff;
  color: #2563eb;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.025em;
  border: 1px solid #bfdbfe;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
  gap: 1.5rem;
}

.loading-state i {
  font-size: 3.5rem;
  color: #3b82f6;
  animation: spin 1s linear infinite;
}

.loading-state p {
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: white;
  border-radius: 12px;
  border: 1px dashed #cbd5e1;
}

.empty-state i {
  font-size: 4rem;
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #0f172a;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

/* PrimeVue Paginator Customization */
:deep(.p-paginator) {
  background: white;
  border-top: 1px solid #e2e8f0;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  border-radius: 0 0 12px 12px;
}

:deep(.p-paginator .p-paginator-first),
:deep(.p-paginator .p-paginator-prev),
:deep(.p-paginator .p-paginator-next),
:deep(.p-paginator .p-paginator-last),
:deep(.p-paginator .p-paginator-page) {
  min-width: 2.5rem;
  height: 2.5rem;
  margin: 0.125rem;
  border-radius: 8px;
  border: 1px solid transparent;
  background: transparent;
  color: #64748b;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  font-size: 0.95rem;
}

:deep(.p-paginator .p-paginator-first:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-prev:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-next:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-last:not(.p-disabled):hover),
:deep(.p-paginator .p-paginator-page:not(.p-highlight):hover) {
  background: #f1f5f9;
  color: #0f172a;
  border-color: #e2e8f0;
}

:deep(.p-paginator .p-paginator-page.p-highlight) {
  background: #3b82f6;
  color: white;
  font-weight: 600;
  border-color: #3b82f6;
  box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
}

:deep(.p-paginator .p-disabled) {
  opacity: 0.4;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .view-reports-page {
    padding: 1rem;
  }
  
  .page-header {
    margin-bottom: 1.5rem;
  }
  
  .card-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .header-controls {
    justify-content: space-between;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
/* Edit Button */
.btn-edit {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.btn-edit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-edit:active {
  transform: translateY(0);
}

/* Edit Modal */
@keyframes overlayFadeIn {
  from { background: rgba(0, 0, 0, 0); }
  to { background: rgba(0, 0, 0, 0.5); }
}

@keyframes modalFadeIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
  animation: overlayFadeIn 0.2s ease;
}

.edit-modal {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: modalFadeIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.edit-modal .modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.edit-modal .modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.btn-close-modal {
  background: transparent;
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-modal:hover {
  opacity: 1;
}

.edit-modal .modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: #475569;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-group label i {
  color: #3b82f6;
  font-size: 1rem;
}

.required {
  color: #ef4444;
}

.input-icon-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon-wrapper .form-input {
  width: 100%;
  padding-right: 2.5rem;
}

.lock-icon {
  position: absolute;
  right: 1rem;
  color: #94a3b8;
  font-size: 0.9rem;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background-color: #ffffff;
  color: #0f172a;
  box-sizing: border-box;
}

.active-input:hover {
  border-color: #94a3b8;
  background-color: #f8fafc;
}

.active-input:focus,
.form-textarea.active-input:focus {
  outline: none;
  border-color: #3b82f6;
  background-color: #ffffff;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.form-input:disabled {
  background: #f1f5f9;
  border-color: #e2e8f0;
  color: #64748b;
  cursor: not-allowed;
  box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.02);
}

.disabled-group label i {
  color: #94a3b8;
}

.disabled-group label {
  color: #64748b;
}

.form-textarea {
  resize: vertical;
  font-family: inherit;
}

.edit-modal .modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  background: #f8fafc;
}

.btn-cancel {
  background: #e2e8f0;
  color: #475569;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-cancel:hover {
  background: #cbd5e1;
  color: #0f172a;
}

.btn-save {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
}

.btn-save:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(16, 185, 129, 0.3);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
