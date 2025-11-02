<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 p-3 sm:p-4 md:p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 sm:mb-6 md:mb-8">
      <div class="flex items-center gap-2 sm:gap-3">
        <button @click="goBack" class="inline-flex items-center text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 px-2 py-1 sm:px-0 transition-colors">
          <span class="material-icons-outlined text-lg sm:text-xl">arrow_back</span>
          <span class="ml-1 text-sm sm:text-base">Back</span>
        </button>
        <h1 class="text-xl sm:text-2xl font-semibold text-gray-800 dark:text-white">Location Management</h1>
      </div>
      <button 
        @click="openCreateModal"
        class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
      >
        <span class="material-icons-outlined text-sm">add</span>
        <span class="text-sm sm:text-base">Add Location</span>
      </button>
    </div>

    <!-- Locations Table -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 sm:p-6 w-full">
      <div v-if="loading" class="text-center py-8">
        <span class="material-icons-outlined animate-spin text-4xl text-gray-400">refresh</span>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Loading locations...</p>
      </div>

      <div v-else-if="locations.length === 0" class="text-center py-8">
        <span class="material-icons-outlined text-6xl text-gray-300 dark:text-gray-600">location_on</span>
        <p class="mt-4 text-gray-600 dark:text-gray-400">No locations found. Create your first location!</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                #
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Location (Department)
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Personnel
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="(location, index) in locations" :key="location.id || location.location_id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ (pagination.current_page - 1) * pagination.per_page + index + 1 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                <div class="flex items-center gap-2">
                  <span class="material-icons-outlined text-base text-gray-400">location_on</span>
                  {{ location.location }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                <div v-if="location.personnel" class="flex items-center gap-2">
                  <span class="material-icons-outlined text-base text-gray-400">person</span>
                  {{ location.personnel }}
                </div>
                <span v-else class="text-gray-400 dark:text-gray-500 italic">Not assigned</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="openEditModal(location)"
                    class="px-3 py-1.5 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors flex items-center gap-1"
                    title="Edit Location"
                  >
                    <span class="material-icons-outlined text-base">edit</span>
                    <span class="hidden sm:inline">Edit</span>
                  </button>
                  <button 
                    @click="confirmDelete(location)"
                    class="px-3 py-1.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors flex items-center gap-1"
                    title="Delete Location"
                  >
                    <span class="material-icons-outlined text-base">delete</span>
                    <span class="hidden sm:inline">Delete</span>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Controls -->
      <div v-if="!loading && locations.length > 0" class="flex flex-col sm:flex-row sm:items-center sm:justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-700 gap-3 sm:gap-0">
        <div class="text-sm text-gray-600 dark:text-gray-300">
          Result {{ (pagination.current_page - 1) * pagination.per_page + 1 }}-{{ Math.min(pagination.current_page * pagination.per_page, pagination.total) }} of {{ pagination.total }}
        </div>
        <div class="flex items-center justify-center sm:justify-end gap-1 flex-wrap">
          <button 
            @click="changePage(1)"
            :disabled="pagination.current_page === 1"
            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            First
          </button>
          <button 
            @click="changePage(pagination.current_page - 1)"
            :disabled="pagination.current_page === 1"
            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            &lt; Previous
          </button>
          <div class="flex items-center gap-1">
            <template v-for="page in pagination.last_page" :key="page">
              <!-- Show first page, last page, current page, and pages around current -->
              <button 
                v-if="page === 1 || page === pagination.last_page || (page >= pagination.current_page - 1 && page <= pagination.current_page + 1)"
                @click="changePage(page)"
                :class="[
                  'px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded hover:bg-gray-50 dark:hover:bg-gray-700',
                  pagination.current_page === page ? 'bg-green-600 text-white border-green-500' : ''
                ]"
              >
                {{ page }}
              </button>
              <!-- Show dots for skipped pages -->
              <span 
                v-else-if="page === pagination.current_page - 2 || page === pagination.current_page + 2"
                class="px-2"
              >...</span>
            </template>
          </div>
          <button 
            @click="changePage(pagination.current_page + 1)"
            :disabled="pagination.current_page === pagination.last_page"
            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            Next &gt;
          </button>
          <button 
            @click="changePage(pagination.last_page)"
            :disabled="pagination.current_page === pagination.last_page"
            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            Last
          </button>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeModal">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 max-w-md w-full">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg sm:text-xl font-semibold text-gray-800 dark:text-white">
            {{ isEditing ? 'Edit Location' : 'Add New Location' }}
          </h2>
          <button @click="closeModal" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
            <span class="material-icons-outlined">close</span>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Location Name -->
          <div class="form-group">
            <label class="form-label">Location Name (Department)</label>
            <div class="relative flex items-center">
              <span class="absolute left-4 text-gray-400">
                <span class="material-icons-outlined">location_on</span>
              </span>
              <input
                v-model="formData.location"
                type="text"
                placeholder="Enter location/department name"
                class="form-input !pl-12"
                required
                :disabled="isSubmitting"
              />
            </div>
            <p v-if="errors.location" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.location[0] }}</p>
          </div>

          <!-- Personnel Name -->
          <div class="form-group">
            <label class="form-label">Personnel Name</label>
            <div class="relative flex items-center">
              <span class="absolute left-4 text-gray-400">
                <span class="material-icons-outlined">person</span>
              </span>
              <input
                v-model="formData.personnel"
                type="text"
                placeholder="Enter personnel name"
                class="form-input !pl-12"
                :disabled="isSubmitting"
              />
            </div>
            <p v-if="errors.personnel" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.personnel[0] }}</p>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end gap-3">
            <button 
              type="button"
              @click="closeModal"
              :disabled="isSubmitting"
              class="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button 
              type="submit"
              :disabled="isSubmitting"
              class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-75 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <span v-if="isSubmitting" class="material-icons-outlined animate-spin text-sm">refresh</span>
              {{ isSubmitting ? (isEditing ? 'Updating...' : 'Creating...') : (isEditing ? 'Update' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click.self="closeDeleteModal">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 max-w-md w-full">
        <div class="flex items-center gap-4 mb-4">
          <div class="w-12 h-12 bg-red-100 dark:bg-red-900/20 rounded-full flex items-center justify-center">
            <span class="material-icons-outlined text-red-600 dark:text-red-400">warning</span>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Delete Location</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">This action cannot be undone.</p>
          </div>
        </div>
        
        <p class="mb-6 text-gray-700 dark:text-gray-300">
          Are you sure you want to delete <strong>"{{ locationToDelete?.location }}"</strong>?
          <span v-if="locationToDelete?.items_count || locationToDelete?.users_count" class="block mt-2 text-red-600 dark:text-red-400 text-sm">
            This location is used by 
            <span v-if="locationToDelete.items_count">{{ locationToDelete.items_count }} item(s)</span>
            <span v-if="locationToDelete.items_count && locationToDelete.users_count"> and </span>
            <span v-if="locationToDelete.users_count">{{ locationToDelete.users_count }} user(s)</span>.
            Deletion will fail.
          </span>
        </p>

        <div class="flex justify-end gap-3">
          <button 
            @click="closeDeleteModal"
            :disabled="isDeleting"
            class="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
          <button 
            @click="handleDelete"
            :disabled="isDeleting"
            class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-75 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <span v-if="isDeleting" class="material-icons-outlined animate-spin text-sm">refresh</span>
            {{ isDeleting ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Success Modal -->
    <SuccessModal
      :isOpen="showSuccessModal"
      :title="successModalType === 'success' ? 'Success' : 'Error'"
      :message="successMessage"
      buttonText="OK"
      :type="successModalType"
      @confirm="closeSuccessModal"
      @close="closeSuccessModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axiosClient from '../axios'
import useLocations from '../composables/useLocations'
import SuccessModal from '../components/SuccessModal.vue'

const router = useRouter()
const { locations, pagination, loading, fetchLocations } = useLocations()

const currentPage = ref(1)
const perPage = 10 // Fixed to 10 items per page
const showModal = ref(false)
const showDeleteModal = ref(false)
const showSuccessModal = ref(false)
const isEditing = ref(false)
const isSubmitting = ref(false)
const isDeleting = ref(false)
const errors = ref({})
const successMessage = ref('')
const successModalType = ref('success')
const locationToDelete = ref(null)

const formData = ref({
  id: null,
  location: '',
  personnel: ''
})

const goBack = () => {
  router.push('/inventory')
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = { id: null, location: '', personnel: '' }
  errors.value = {}
  showModal.value = true
}

const openEditModal = (location) => {
  isEditing.value = true
  formData.value = {
    id: location.id || location.location_id,
    location: location.location,
    personnel: location.personnel || ''
  }
  errors.value = {}
  showModal.value = true
}

const closeModal = () => {
  if (isSubmitting.value) return
  showModal.value = false
  formData.value = { id: null, location: '', personnel: '' }
  errors.value = {}
  isEditing.value = false
}

const confirmDelete = (location) => {
  locationToDelete.value = location
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  if (isDeleting.value) return
  showDeleteModal.value = false
  locationToDelete.value = null
}

const handleSubmit = async () => {
  if (isSubmitting.value) return
  
  try {
    isSubmitting.value = true
    errors.value = {}

    if (!formData.value.location.trim()) {
      errors.value.location = ['Location name is required']
      isSubmitting.value = false
      return
    }

    const payload = {
      location: formData.value.location.trim(),
      personnel: formData.value.personnel?.trim() || null
    }

    let response
    if (isEditing.value) {
      response = await axiosClient.put(`/locations/${formData.value.id}`, payload)
    } else {
      response = await axiosClient.post('/locations', payload)
    }

    if (response.data?.success) {
      successMessage.value = isEditing.value 
        ? 'Location updated successfully!' 
        : 'Location created successfully!'
      successModalType.value = 'success'
      showSuccessModal.value = true
      
      await fetchLocations(currentPage.value, perPage)
      closeModal()
    }
  } catch (error) {
    console.error('Error saving location:', error)
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else if (error.response?.data?.message) {
      errors.value = {
        location: [error.response.data.message]
      }
      successMessage.value = error.response.data.message
      successModalType.value = 'error'
      showSuccessModal.value = true
    } else {
      errors.value = {
        location: ['An unexpected error occurred. Please try again.']
      }
      successMessage.value = 'An unexpected error occurred. Please try again.'
      successModalType.value = 'error'
      showSuccessModal.value = true
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleDelete = async () => {
  if (isDeleting.value || !locationToDelete.value) return
  
  try {
    isDeleting.value = true
    const locationId = locationToDelete.value.id || locationToDelete.value.location_id
    
    const response = await axiosClient.delete(`/locations/${locationId}`)
    
    if (response.data?.success) {
      successMessage.value = 'Location deleted successfully!'
      successModalType.value = 'success'
      showSuccessModal.value = true
      
      await fetchLocations(currentPage.value, perPage)
      closeDeleteModal()
    }
  } catch (error) {
    console.error('Error deleting location:', error)
    
    if (error.response?.data?.message) {
      successMessage.value = error.response.data.message
      successModalType.value = 'error'
      showSuccessModal.value = true
    } else {
      successMessage.value = 'Failed to delete location. Please try again.'
      successModalType.value = 'error'
      showSuccessModal.value = true
    }
  } finally {
    isDeleting.value = false
  }
}

const closeSuccessModal = () => {
  showSuccessModal.value = false
  successMessage.value = ''
  successModalType.value = 'success'
}

const changePage = async (page) => {
  currentPage.value = page
  await fetchLocations(page, perPage)
}

// Removed changePerPage - fixed to 10 items per page

onMounted(async () => {
  await fetchLocations(currentPage.value, perPage)
})
</script>

<style scoped>
.form-group {
  @apply space-y-1;
}

.form-label {
  @apply block text-sm font-medium text-gray-700 dark:text-gray-300;
}

.form-input {
  @apply block w-full rounded-lg border-gray-200 dark:border-gray-600 shadow-sm focus:border-green-500 focus:ring-green-500 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white;
  height: 45px;
}

.material-icons-outlined {
  font-size: 20px;
}
</style>

