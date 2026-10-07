import { useEffect, useState } from "react"

import {
  getProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../services/productService"

function Products() {
  const [products, setProducts] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [showForm, setShowForm] = useState(false)
  const [editingProduct, setEditingProduct] = useState(null)

  const [formData, setFormData] = useState({
    name: "",
    price: "",
    category: "",
  })

  const loadProducts = async () => {
    try {
      setLoading(true)
      setError(null)

      const data = await getProducts()
      setProducts(data)
    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to load products"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadProducts()
  }, [])

  const handleInputChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))
  }

  const resetForm = () => {
    setFormData({
      name: "",
      price: "",
      category: "",
    })

    setEditingProduct(null)
    setShowForm(false)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      setError(null)

      const productData = {
        name: formData.name,
        price: Number(formData.price),
        category: formData.category,
      }

      if (editingProduct) {
        await updateProduct(
          editingProduct.id,
          productData
        )
      } else {
        await createProduct(productData)
      }

      resetForm()
      await loadProducts()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to save product"
      )
    }
  }

  const handleEdit = (product) => {
    setEditingProduct(product)

    setFormData({
      name: product.name,
      price: product.price,
      category: product.category,
    })

    setShowForm(true)
  }

  const handleDelete = async (productId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this product?"
    )

    if (!confirmed) {
      return
    }

    try {
      setError(null)

      await deleteProduct(productId)

      await loadProducts()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to delete product"
      )
    }
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Products
          </h1>

          <p className="mt-2 text-slate-600">
            Manage products and product information
          </p>
        </div>

        <button
          onClick={() => {
            setEditingProduct(null)

            setFormData({
              name: "",
              price: "",
              category: "",
            })

            setShowForm(true)
          }}
          className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
        >
          + Add Product
        </button>

      </div>

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Product Form */}
      {showForm && (
        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

          <div className="mb-6">
            <h2 className="text-xl font-semibold text-slate-900">
              {editingProduct
                ? "Edit Product"
                : "Add Product"}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Enter the product details below.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-5 md:grid-cols-3"
          >

            {/* Name */}
            <div>
              <label
                htmlFor="name"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Product Name
              </label>

              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter product name"
              />
            </div>

            {/* Price */}
            <div>
              <label
                htmlFor="price"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Price
              </label>

              <input
                id="price"
                name="price"
                type="number"
                min="0"
                step="0.01"
                value={formData.price}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter price"
              />
            </div>

            {/* Category */}
            <div>
              <label
                htmlFor="category"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Category
              </label>

              <input
                id="category"
                name="category"
                type="text"
                value={formData.category}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter category"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3 md:col-span-3">

              <button
                type="submit"
                className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700"
              >
                {editingProduct
                  ? "Update Product"
                  : "Create Product"}
              </button>

              <button
                type="button"
                onClick={resetForm}
                className="rounded-lg border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              >
                Cancel
              </button>

            </div>

          </form>

        </section>
      )}

      {/* Product Table */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="border-b border-slate-200 px-6 py-5">

          <h2 className="text-lg font-semibold text-slate-900">
            Product List
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {products.length} products
          </p>

        </div>

        {loading ? (
          <div className="p-6 text-sm text-slate-500">
            Loading products...
          </div>
        ) : products.length === 0 ? (
          <div className="p-6 text-sm text-slate-500">
            No products found.
          </div>
        ) : (
          <div className="overflow-x-auto">

            <table className="min-w-full text-left text-sm">

              <thead className="bg-slate-50 text-xs uppercase text-slate-500">

                <tr>
                  <th className="px-6 py-4">
                    ID
                  </th>

                  <th className="px-6 py-4">
                    Name
                  </th>

                  <th className="px-6 py-4">
                    Category
                  </th>

                  <th className="px-6 py-4">
                    Price
                  </th>

                  <th className="px-6 py-4">
                    Actions
                  </th>
                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {products.map((product) => (
                  <tr
                    key={product.id}
                    className="hover:bg-slate-50"
                  >

                    <td className="px-6 py-4 text-slate-500">
                      #{product.id}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {product.name}
                    </td>

                    <td className="px-6 py-4 text-slate-600">
                      {product.category}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      ₹{Number(product.price).toLocaleString("en-IN")}
                    </td>

                    <td className="px-6 py-4">

                      <div className="flex gap-2">

                        <button
                          onClick={() => handleEdit(product)}
                          className="rounded-md bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-200"
                        >
                          Edit
                        </button>

                        <button
                          onClick={() => handleDelete(product.id)}
                          className="rounded-md bg-red-100 px-3 py-2 text-xs font-medium text-red-700 hover:bg-red-200"
                        >
                          Delete
                        </button>

                      </div>

                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>
        )}

      </section>

    </div>
  )
}

export default Products