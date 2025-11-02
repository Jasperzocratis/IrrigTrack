import { ref, onMounted, watch } from 'vue'
import axiosClient from '../axios' // or wherever your axiosClient is

export default function usecategories(formData = null) {
  const categories = ref([])
  const pagination = ref({
    current_page: 1,
    last_page: 1,
    per_page: 10,
    total: 0,
    from: null,
    to: null
  })
  const loading = ref(false)

  const fetchcategories = async (page = 1, perPage = 10) => {
    try {
      loading.value = true
      const response = await axiosClient.get('/categories', {
        params: {
          page,
          per_page: perPage
        }
      })
      if (response.data && response.data.data) {
        categories.value = response.data.data
        if (response.data.pagination) {
          pagination.value = response.data.pagination
        }
        console.log('Available categories:', categories.value)
      }
    } catch (error) {
      console.error('Error fetching categories:', error)
    } finally {
      loading.value = false
    }
  }

  const createCategory = async (categoryData) => {
    try {
      const response = await axiosClient.post('/categories', categoryData)
      await fetchcategories(pagination.value.current_page, pagination.value.per_page) // Refresh list
      return response.data
    } catch (error) {
      console.error('Error creating category:', error)
      throw error
    }
  }

  const updateCategory = async (id, categoryData) => {
    try {
      const response = await axiosClient.put(`/categories/${id}`, categoryData)
      await fetchcategories(pagination.value.current_page, pagination.value.per_page) // Refresh list
      return response.data
    } catch (error) {
      console.error('Error updating category:', error)
      throw error
    }
  }

  const deleteCategory = async (id) => {
    try {
      const response = await axiosClient.delete(`/categories/${id}`)
      await fetchcategories(pagination.value.current_page, pagination.value.per_page) // Refresh list
      return response.data
    } catch (error) {
      console.error('Error deleting category:', error)
      throw error
    }
  }

  // Note: Pages should call fetchcategories() manually with page and perPage

  if (formData) {
    watch(() => formData.value.category, (newValue) => {
      console.log('Category selected:', newValue)
    })
  }

  return {
    categories,
    pagination,
    loading,
    fetchcategories,
    createCategory,
    updateCategory,
    deleteCategory
  }
}
