import { useEffect, useState } from "react"

import {
  getInventories,
  createInventory,
  updateInventory,
  deleteInventory,
} from "../services/inventoryService"

import { getProducts } from "../services/productService"
import { getWarehouses } from "../services/warehouseService"

function Inventory() {
  const [inventories, setInventories] = useState([])
  const [products, setProducts] = useState([])
  const [warehouses, setWarehouses] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [showForm, setShowForm] = useState(false)
  const [editingInventory, setEditingInventory] = useState(null)

  const [formData, setFormData] = useState({
    product_id: "",
    warehouse_id: "",
    quantity: "",
  })

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [
        inventoryData,
        productData,
        warehouseData,
      ] = await Promise.all([
        getInventories(),
        getProducts(),
        getWarehouses(),
      ])

      setInventories(inventoryData)
      setProducts(productData)
      setWarehouses(warehouseData)
    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to load inventory data"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
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
      product_id: "",
      warehouse_id: "",
      quantity: "",
    })

    setEditingInventory(null)
    setShowForm(false)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      setError(null)

      const inventoryData = {
        product_id: Number(formData.product_id),
        warehouse_id: Number(formData.warehouse_id),
        quantity: Number(formData.quantity),
      }

      if (editingInventory) {
        await updateInventory(
          editingInventory.id,
          inventoryData
        )
      } else {
        await createInventory(inventoryData)
      }

      resetForm()
      await loadData()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to save inventory"
      )
    }
  }

  const handleEdit = (inventory) => {
    setEditingInventory(inventory)

    setFormData({
      product_id: String(inventory.product_id),
      warehouse_id: String(inventory.warehouse_id),
      quantity: String(inventory.quantity),
    })

    setShowForm(true)
  }

  const handleDelete = async (inventoryId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this inventory record?"
    )

    if (!confirmed) {
      return
    }

    try {
      setError(null)

      await deleteInventory(inventoryId)

      await loadData()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to delete inventory"
      )
    }
  }

  const getProductName = (productId) => {
    const product = products.find(
      (item) => item.id === productId
    )

    return product
      ? product.name
      : `Product #${productId}`
  }

  const getWarehouseName = (warehouseId) => {
    const warehouse = warehouses.find(
      (item) => item.id === warehouseId
    )

    return warehouse
      ? warehouse.name
      : `Warehouse #${warehouseId}`
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Inventory
          </h1>

          <p className="mt-2 text-slate-600">
            Manage product stock across warehouses
          </p>
        </div>

        <button
          onClick={() => {
            setEditingInventory(null)

            setFormData({
              product_id: "",
              warehouse_id: "",
              quantity: "",
            })

            setShowForm(true)
          }}
          className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
        >
          + Add Inventory
        </button>

      </div>

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Form */}
      {showForm && (
        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

          <div className="mb-6">
            <h2 className="text-xl font-semibold text-slate-900">
              {editingInventory
                ? "Edit Inventory"
                : "Add Inventory"}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Assign product stock to a warehouse.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-5 md:grid-cols-3"
          >

            {/* Product */}
            <div>
              <label
                htmlFor="product_id"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Product
              </label>

              <select
                id="product_id"
                name="product_id"
                value={formData.product_id}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              >
                <option value="">
                  Select product
                </option>

                {products.map((product) => (
                  <option
                    key={product.id}
                    value={product.id}
                  >
                    {product.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Warehouse */}
            <div>
              <label
                htmlFor="warehouse_id"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Warehouse
              </label>

              <select
                id="warehouse_id"
                name="warehouse_id"
                value={formData.warehouse_id}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 bg-white px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              >
                <option value="">
                  Select warehouse
                </option>

                {warehouses.map((warehouse) => (
                  <option
                    key={warehouse.id}
                    value={warehouse.id}
                  >
                    {warehouse.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Quantity */}
            <div>
              <label
                htmlFor="quantity"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Quantity
              </label>

              <input
                id="quantity"
                name="quantity"
                type="number"
                min="0"
                step="1"
                value={formData.quantity}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter quantity"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3 md:col-span-3">

              <button
                type="submit"
                className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700"
              >
                {editingInventory
                  ? "Update Inventory"
                  : "Create Inventory"}
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

      {/* Inventory Table */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="border-b border-slate-200 px-6 py-5">

          <h2 className="text-lg font-semibold text-slate-900">
            Inventory Records
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {inventories.length} inventory records
          </p>

        </div>

        {loading ? (
          <div className="p-6 text-sm text-slate-500">
            Loading inventory...
          </div>
        ) : inventories.length === 0 ? (
          <div className="p-6 text-sm text-slate-500">
            No inventory records found.
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
                    Product
                  </th>

                  <th className="px-6 py-4">
                    Warehouse
                  </th>

                  <th className="px-6 py-4">
                    Quantity
                  </th>

                  <th className="px-6 py-4">
                    Actions
                  </th>
                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {inventories.map((inventory) => (
                  <tr
                    key={inventory.id}
                    className="hover:bg-slate-50"
                  >

                    <td className="px-6 py-4 text-slate-500">
                      #{inventory.id}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {getProductName(inventory.product_id)}
                    </td>

                    <td className="px-6 py-4 text-slate-600">
                      {getWarehouseName(
                        inventory.warehouse_id
                      )}
                    </td>

                    <td className="px-6 py-4">

                      <span
                        className={
                          inventory.quantity === 0
                            ? "font-semibold text-red-600"
                            : inventory.quantity <= 20
                              ? "font-semibold text-amber-600"
                              : "font-semibold text-slate-900"
                        }
                      >
                        {inventory.quantity}
                      </span>

                    </td>

                    <td className="px-6 py-4">

                      <div className="flex gap-2">

                        <button
                          onClick={() =>
                            handleEdit(inventory)
                          }
                          className="rounded-md bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-200"
                        >
                          Edit
                        </button>

                        <button
                          onClick={() =>
                            handleDelete(inventory.id)
                          }
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

export default Inventory