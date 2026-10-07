import { useEffect, useState } from "react"

import {
  getWarehouses,
  createWarehouse,
  updateWarehouse,
  deleteWarehouse,
} from "../services/warehouseService"

function Warehouses() {
  const [warehouses, setWarehouses] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [showForm, setShowForm] = useState(false)
  const [editingWarehouse, setEditingWarehouse] = useState(null)

  const [formData, setFormData] = useState({
    name: "",
    location: "",
  })

  const loadWarehouses = async () => {
    try {
      setLoading(true)
      setError(null)

      const data = await getWarehouses()
      setWarehouses(data)
    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to load warehouses"
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadWarehouses()
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
      location: "",
    })

    setEditingWarehouse(null)
    setShowForm(false)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      setError(null)

      const warehouseData = {
        name: formData.name,
        location: formData.location,
      }

      if (editingWarehouse) {
        await updateWarehouse(
          editingWarehouse.id,
          warehouseData
        )
      } else {
        await createWarehouse(warehouseData)
      }

      resetForm()
      await loadWarehouses()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to save warehouse"
      )
    }
  }

  const handleEdit = (warehouse) => {
    setEditingWarehouse(warehouse)

    setFormData({
      name: warehouse.name,
      location: warehouse.location,
    })

    setShowForm(true)
  }

  const handleDelete = async (warehouseId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this warehouse?"
    )

    if (!confirmed) {
      return
    }

    try {
      setError(null)

      await deleteWarehouse(warehouseId)

      await loadWarehouses()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to delete warehouse"
      )
    }
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Warehouses
          </h1>

          <p className="mt-2 text-slate-600">
            Manage warehouse locations and information
          </p>
        </div>

        <button
          onClick={() => {
            setEditingWarehouse(null)

            setFormData({
              name: "",
              location: "",
            })

            setShowForm(true)
          }}
          className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
        >
          + Add Warehouse
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
              {editingWarehouse
                ? "Edit Warehouse"
                : "Add Warehouse"}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Enter the warehouse details below.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-5 md:grid-cols-2"
          >

            {/* Name */}
            <div>
              <label
                htmlFor="name"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Warehouse Name
              </label>

              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter warehouse name"
              />
            </div>

            {/* Location */}
            <div>
              <label
                htmlFor="location"
                className="mb-2 block text-sm font-medium text-slate-700"
              >
                Location
              </label>

              <input
                id="location"
                name="location"
                type="text"
                value={formData.location}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter warehouse location"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3 md:col-span-2">

              <button
                type="submit"
                className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700"
              >
                {editingWarehouse
                  ? "Update Warehouse"
                  : "Create Warehouse"}
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

      {/* Warehouse Table */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="border-b border-slate-200 px-6 py-5">

          <h2 className="text-lg font-semibold text-slate-900">
            Warehouse List
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {warehouses.length} warehouses
          </p>

        </div>

        {loading ? (
          <div className="p-6 text-sm text-slate-500">
            Loading warehouses...
          </div>
        ) : warehouses.length === 0 ? (
          <div className="p-6 text-sm text-slate-500">
            No warehouses found.
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
                    Location
                  </th>

                  <th className="px-6 py-4">
                    Actions
                  </th>
                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {warehouses.map((warehouse) => (
                  <tr
                    key={warehouse.id}
                    className="hover:bg-slate-50"
                  >

                    <td className="px-6 py-4 text-slate-500">
                      #{warehouse.id}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {warehouse.name}
                    </td>

                    <td className="px-6 py-4 text-slate-600">
                      {warehouse.location}
                    </td>

                    <td className="px-6 py-4">

                      <div className="flex gap-2">

                        <button
                          onClick={() => handleEdit(warehouse)}
                          className="rounded-md bg-slate-100 px-3 py-2 text-xs font-medium text-slate-700 hover:bg-slate-200"
                        >
                          Edit
                        </button>

                        <button
                          onClick={() =>
                            handleDelete(warehouse.id)
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

export default Warehouses