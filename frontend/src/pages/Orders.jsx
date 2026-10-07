import { useEffect, useState } from "react"

import {
  getOrders,
  createOrder,
  cancelOrder,
} from "../services/orderService"

import { getProducts } from "../services/productService"

function Orders() {
  const [orders, setOrders] = useState([])
  const [products, setProducts] = useState([])

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [showForm, setShowForm] = useState(false)

  const [formData, setFormData] = useState({
    product_id: "",
    quantity: "",
  })

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      const [orderData, productData] = await Promise.all([
        getOrders(),
        getProducts(),
      ])

      setOrders(orderData)
      setProducts(productData)
    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to load orders"
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
      quantity: "",
    })

    setShowForm(false)
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    try {
      setError(null)

      const orderData = {
        product_id: Number(formData.product_id),
        quantity: Number(formData.quantity),
      }

      await createOrder(orderData)

      resetForm()
      await loadData()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to create order"
      )
    }
  }

  const handleCancel = async (orderId) => {
    const confirmed = window.confirm(
      "Cancel this order? Allocated inventory will be restored."
    )

    if (!confirmed) {
      return
    }

    try {
      setError(null)

      await cancelOrder(orderId)

      await loadData()

    } catch (err) {
      console.error(err)

      setError(
        err.response?.data?.message ||
        err.message ||
        "Failed to cancel order"
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

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

        <div>
          <h1 className="text-3xl font-bold text-slate-900">
            Orders
          </h1>

          <p className="mt-2 text-slate-600">
            Manage customer orders and inventory allocation
          </p>
        </div>

        <button
          onClick={() => {
            setFormData({
              product_id: "",
              quantity: "",
            })

            setError(null)
            setShowForm(true)
          }}
          className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
        >
          + Create Order
        </button>

      </div>

      {/* Error */}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          <p className="font-semibold">
            Order operation failed
          </p>

          <p className="mt-1">
            {error}
          </p>
        </div>
      )}

      {/* Create Order Form */}
      {showForm && (
        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

          <div className="mb-6">
            <h2 className="text-xl font-semibold text-slate-900">
              Create Order
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              The backend will automatically allocate inventory
              across available warehouses.
            </p>
          </div>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-1 gap-5 md:grid-cols-2"
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
                min="1"
                step="1"
                value={formData.quantity}
                onChange={handleInputChange}
                required
                className="w-full rounded-lg border border-slate-300 px-4 py-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Enter quantity"
              />
            </div>

            {/* Actions */}
            <div className="flex gap-3 md:col-span-2">

              <button
                type="submit"
                className="rounded-lg bg-blue-600 px-5 py-3 text-sm font-semibold text-white hover:bg-blue-700"
              >
                Create Order
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

      {/* Orders Table */}
      <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">

        <div className="border-b border-slate-200 px-6 py-5">

          <h2 className="text-lg font-semibold text-slate-900">
            Order List
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            {orders.length} orders
          </p>

        </div>

        {loading ? (
          <div className="p-6 text-sm text-slate-500">
            Loading orders...
          </div>
        ) : orders.length === 0 ? (
          <div className="p-6 text-sm text-slate-500">
            No orders found.
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
                    Quantity
                  </th>

                  <th className="px-6 py-4">
                    Status
                  </th>

                  <th className="px-6 py-4">
                    Actions
                  </th>
                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {orders.map((order) => (
                  <tr
                    key={order.id}
                    className="hover:bg-slate-50"
                  >

                    <td className="px-6 py-4 text-slate-500">
                      #{order.id}
                    </td>

                    <td className="px-6 py-4 font-medium text-slate-900">
                      {getProductName(order.product_id)}
                    </td>

                    <td className="px-6 py-4 font-semibold text-slate-900">
                      {order.quantity}
                    </td>

                    <td className="px-6 py-4">

                      {order.status === "CONFIRMED" ? (
                        <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                          CONFIRMED
                        </span>
                      ) : (
                        <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-700">
                          {order.status}
                        </span>
                      )}

                    </td>

                    <td className="px-6 py-4">

                      {order.status === "CONFIRMED" ? (
                        <button
                          onClick={() =>
                            handleCancel(order.id)
                          }
                          className="rounded-md bg-red-100 px-3 py-2 text-xs font-medium text-red-700 hover:bg-red-200"
                        >
                          Cancel Order
                        </button>
                      ) : (
                        <span className="text-xs text-slate-400">
                          No actions available
                        </span>
                      )}

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

export default Orders