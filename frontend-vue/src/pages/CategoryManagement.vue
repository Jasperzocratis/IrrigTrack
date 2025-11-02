<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 p-3 sm:p-4 md:p-6">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 sm:mb-6 md:mb-8">
      <div class="flex items-center gap-2 sm:gap-3">
        <button @click="goBack" class="inline-flex items-center text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 px-2 py-1 sm:px-0 transition-colors">
          <span class="material-icons-outlined text-lg sm:text-xl">arrow_back</span>
          <span class="ml-1 text-sm sm:text-base">Back</span>
        </button>
        <h1 class="text-xl sm:text-2xl font-semibold text-gray-800 dark:text-white">Category Management</h1>
      </div>
      <button 
        @click="openCreateModal"
        class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors flex items-center gap-2"
      >
        <span class="material-icons-outlined text-sm">add</span>
        <span class="text-sm sm:text-base">Add Category</span>
      </button>
    </div>

    <!-- Categories Table -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-4 sm:p-6 w-full">
      <div v-if="loading" class="text-center py-8">
        <span class="material-icons-outlined animate-spin text-4xl text-gray-400">refresh</span>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Loading categories...</p>
      </div>

      <div v-else-if="categories.length === 0" class="text-center py-8">
        <span class="material-icons-outlined text-6xl text-gray-300 dark:text-gray-600">category</span>
        <p class="mt-4 text-gray-600 dark:text-gray-400">No categories found. Create your first category!</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                #
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Category Name
              </th>
              <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="(category, index) in categories" :key="category.id || category.category_id" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ (pagination.current_page - 1) * pagination.per_page + index + 1 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-white">
                <div class="flex items-center gap-2">
                  <span class="material-icons-outlined text-base text-gray-400">label</span>
                  {{ category.category }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="openEditModal(category)"
                    class="px-3 py-1.5 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors flex items-center gap-1"
                    title="Edit Category"
                  >
                    <span class="material-icons-outlined text-base">edit</span>
                    <span class="hidden sm:inline">Edit</span>
                  </button>
                  <button 
                    @click="confirmDelete(category)"
                    class="px-3 py-1.5 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors flex items-center gap-1"
                    title="Delete Category"
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
      <div v-if="!loading && categories.length > 0" class="flex flex-col sm:flex-row sm:items-center sm:justify-between px-4 py-3 border-t border-gray-200 dark:border-gray-700 gap-3 sm:gap-0">
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
            {{ isEditing ? 'Edit Category' : 'Add New Category' }}
          </h2>
          <button @click="closeModal" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
            <span class="material-icons-outlined">close</span>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Category Name -->
          <div class="form-group">
            <label class="form-label">Category Name</label>
            <div class="relative flex items-center">
              <span class="absolute left-4 text-gray-400">
                <span class="material-icons-outlined">category</span>
              </span>
              <input
                v-model="formData.category"
                type="text"
                placeholder="Enter category name"
                class="form-input !pl-12"
                required
                :disabled="isSubmitting"
              />
            </div>
            <p v-if="errors.category" class="mt-1 text-sm text-red-600 dark:text-red-400">{{ errors.category[0] }}</p>
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
            <h3 class="text-lg font-semibold text-gray-800 dark:text-white">Delete Category</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">This action cannot be undone.</p>
          </div>
        </div>
        
        <p class="mb-6 text-gray-700 dark:text-gray-300">
          Are you sure you want to delete <strong>"{{ categoryToDelete?.category }}"</strong>?
          <span v-if="categoryToDelete?.items_count" class="block mt-2 text-red-600 dark:text-red-400 text-sm">
            This category is used by {{ categoryToDelete.items_count }} item(s). Deletion will fail.
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
import useCategories from '../composables/useCategories'
import SuccessModal from '../components/SuccessModal.vue'

const router = useRouter()
const { categories, pagination, loading, fetchcategories } = useCategories()

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
const categoryToDelete = ref(null)

const formData = ref({
  id: null,
  category: ''
})

const goBack = () => {
  router.push('/inventory')
}

const openCreateModal = () => {
  isEditing.value = false
  formData.value = { id: null, category: '' }
  errors.value = {}
  showModal.value = true
}

const openEditModal = (category) => {
  isEditing.value = true
  formData.value = {
    id: category.id || category.category_id,
    category: category.category
  }
  errors.value = {}
  showModal.value = true
}

const closeModal = () => {
  if (isSubmitting.value) return
  showModal.value = false
  formData.value = { id: null, category: '' }
  errors.value = {}
  isEditing.value = false
}

const confirmDelete = (category) => {
  categoryToDelete.value = category
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  if (isDeleting.value) return
  showDeleteModal.value = false
  categoryToDelete.value = null
}

const handleSubmit = async () => {
  if (isSubmitting.value) return
  
  try {
    isSubmitting.value = true
    errors.value = {}

    if (!formData.value.category.trim()) {
      errors.value.category = ['Category name is required']
      isSubmitting.value = false
      return
    }

    let response
    if (isEditing.value) {
      response = await axiosClient.put(`/categories/${formData.value.id}`, {
        category: formData.value.category.trim()
      })
    } else {
      response = await axiosClient.post('/categories', {
        category: formData.value.category.trim()
      })
    }

    if (response.data?.success) {
      successMessage.value = isEditing.value 
        ? 'Category updated successfully!' 
        : 'Category created successfully!'
      successModalType.value = 'success'
      showSuccessModal.value = true
      
      await fetchcategories(currentPage.value, perPage)
      closeModal()
    }
  } catch (error) {
    console.error('Error saving category:', error)
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else if (error.response?.data?.message) {
      errors.value = {
        category: [error.response.data.message]
      }
      successMessage.value = error.response.data.message
      successModalType.value = 'error'
      showSuccessModal.value = true
    } else {
      errors.value = {
        category: ['An unexpected error occurred. Please try again.']
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
  if (isDeleting.value || !categoryToDelete.value) return
  
  try {
    isDeleting.value = true
    const categoryId = categoryToDelete.value.id || categoryToDelete.value.category_id
    
    const response = await axiosClient.delete(`/categories/${categoryId}`)
    
    if (response.data?.success) {
      successMessage.value = 'Category deleted successfully!'
      successModalType.value = 'success'
      showSuccessModal.value = true
      
      await fetchcategories(currentPage.value, perPage)
      closeDeleteModal()
    }
  } catch (error) {
    console.error('Error deleting category:', error)
    
    if (error.response?.data?.message) {
      successMessage.value = error.response.data.message
      successModalType.value = 'error'
      showSuccessModal.value = true
    } else {
      successMessage.value = 'Failed to delete category. Please try again.'
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
  await fetchcategories(page, perPage)
}

// Removed changePerPage - fixed to 10 items per page

onMounted(async () => {
  await fetchcategories(currentPage.value, perPage)
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

