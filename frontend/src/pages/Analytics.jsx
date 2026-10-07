import { useEffect, useState } from "react"
import {
  getInventorySummary,
  getLowStockInventory,
  getInventoryInsight,
} from "../services/analyticsService"

function Analytics() {
  const [summary, setSummary] = useState(null)
  const [lowStock, setLowStock] = useState([])
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setLoading(true)
        setError("")

        const [summaryData, lowStockData, insightsData] =
          await Promise.all([
            getInventorySummary(),
            getLowStockInventory(20),
            getInventoryInsight(20),
          ])

        setSummary(summaryData)
        setLowStock(lowStockData)
        setInsights(insightsData)
      } catch (err) {
        console.error(err)
        setError("Failed to load analytics data.")
      } finally {
        setLoading(false)
      }
    }

    loadAnalytics()
  }, [])

  if (loading) {
    return (
      <div className="p-6">
        <p className="text-slate-600">Loading analytics...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <p className="text-red-600">{error}</p>
      </div>
    )
  }

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Analytics
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Inventory and operational insights
        </p>
      </div>

      {/* Summary */}
      <section>
        <h2 className="mb-4 text-lg font-semibold text-slate-900">
          Business Summary
        </h2>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <MetricCard
            title="Total Products"
            value={summary?.total_products}
          />

          <MetricCard
            title="Total Warehouses"
            value={summary?.total_warehouses}
          />

          <MetricCard
            title="Inventory Units"
            value={summary?.total_inventory_units}
          />

          <MetricCard
            title="Total Orders"
            value={summary?.total_orders}
          />

          <MetricCard
            title="Ordered Units"
            value={summary?.total_order_units}
          />

          <MetricCard
            title="Inventory Value"
            value={summary?.total_inventory_value}
          />
        </div>
      </section>

      {/* Low Stock */}
      <section>
        <h2 className="mb-4 text-lg font-semibold text-slate-900">
          Low Stock Inventory
        </h2>

        <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white">
          <table className="min-w-full text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-4 py-3 text-left">Product</th>
                <th className="px-4 py-3 text-left">Warehouse</th>
                <th className="px-4 py-3 text-left">Quantity</th>
                <th className="px-4 py-3 text-left">Threshold</th>
              </tr>
            </thead>

            <tbody>
              {lowStock.map((item) => (
                <tr
                  key={`${item.product_id}-${item.warehouse_id}`}
                  className="border-t border-slate-100"
                >
                  <td className="px-4 py-3">
                    {item.product_name}
                  </td>

                  <td className="px-4 py-3">
                    {item.warehouse_name}
                  </td>

                  <td className="px-4 py-3 font-semibold text-red-600">
                    {item.quantity}
                  </td>

                  <td className="px-4 py-3">
                    {item.threshold}
                  </td>
                </tr>
              ))}

              {lowStock.length === 0 && (
                <tr>
                  <td
                    colSpan="4"
                    className="px-4 py-6 text-center text-slate-500"
                  >
                    No low-stock inventory.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* Insights */}
      <section>
        <h2 className="mb-4 text-lg font-semibold text-slate-900">
          Inventory Insights
        </h2>

        <div className="space-y-3">
          {insights.map((item) => (
            <div
              key={`${item.product_id}-${item.warehouse_id}`}
              className="rounded-lg border border-red-200 bg-red-50 p-4"
            >
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-red-800">
                  {item.severity}
                </h3>

                <span className="text-sm font-medium text-red-700">
                  Qty: {item.quantity}
                </span>
              </div>

              <p className="mt-2 text-sm text-red-700">
                {item.recommendation}
              </p>
            </div>
          ))}

          {insights.length === 0 && (
            <div className="rounded-lg border border-slate-200 bg-white p-4 text-slate-500">
              No critical inventory insights.
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

function MetricCard({ title, value }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5">
      <p className="text-sm text-slate-500">{title}</p>

      <p className="mt-2 whitespace-nowrap text-2xl font-bold tracking-tight text-slate-900">
        {value}
      </p>
    </div>
  )
}

export default Analytics