import { useEffect, useState } from "react"

import {
    getInventorySummary,
    getLowStockInventory,
    getInventoryInsight
} from "../services/analyticsService"

function Dashboard() {

    const [summary, setSummary] = useState(null)
    const [lowStock, setLowStock] = useState([])
    const [insights, setInventoryInsight] = useState([])

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const loadDashboard = async () => {
            try {
                const [
                    summaryData,
                    lowStockData,
                    inventoryInsightData
                ] = await Promise.all([
                    getInventorySummary(),
                    getLowStockInventory(),
                    getInventoryInsight()
                ])

                setSummary(summaryData),
                    setLowStock(lowStockData),
                    setInventoryInsight(inventoryInsightData)
            }

            catch (err) {
                console.error(err)

                setError(
                    err.response?.data?.message ||
                    err.message ||
                    "Failed to load dashboard data"
                )
            }
            finally {
                setLoading(false)
            }
        }

        loadDashboard()
    }, [])

    if (loading) {
        return (

            <div>
                <h1 className="text-2xl font-bold text-slate-900">
                    Dashboard
                </h1>

                <p className="mt-2 text-slate-600">
                    Inventory and Operations Overview
                </p>
            </div>
        )
    }

    if (error) {
        return (
            <div>
                <h1 className="text-2xl font-bold text-slate-900">
                    Dashboard
                </h1>

                <div className="mt-6 rounded border border-red-200 bg-red-50 p-4 text-red-700">
                    <p className="font-semibold">
                        Failed to load dashboard
                    </p>

                    <p className="mt-1 text-sm">
                        {error}
                    </p>
                </div>
            </div>
        )
    }

    return (
        <div className="space-y-8">
            {/*Header*/}

            <div>
                <h1 className="text-3xl font-bold text-slate-900">
                    Dashboard
                </h1>

                <p className="mt-2 text-slate-600">
                    Inventory and Operations Overview
                </p>
            </div>

            {/*KPI Cards*/}
            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
                <KpiCard
                    title="Products"
                    value={summary.total_products}
                />
                <KpiCard
                    title="Warehouses"
                    value={summary.total_warehouses}
                />
                <KpiCard
                    title="Inventory Units"
                    value={summary.total_inventory_units}
                />
                <KpiCard
                    title="Orders"
                    value={summary.total_orders}
                />
                <KpiCard
                    title="Order units"
                    value={summary.total_order_units}
                />
                <KpiCard
                    title="Total Inventory"
                    value={`₹${summary.total_inventory_value.toLocaleString("en-IN")}`}
                />
            </div>

            {/*Low Stock*/}
            <section className="rounded-xl border border-slate-200 bg-white shadow-sm">
                <div className="border-b border-slate-200 px-6 py-5">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-lg font-semibold text-slate-900">
                                Low Stock Inventory
                            </h1>

                            <p className="mt-1 text-sm text-slate-500">
                                Products below are configured inventory threshold
                            </p>
                        </div>

                        <span className="rounded-full bg-amber-100 px-3 py-3 text-sm font-medium text-amber-700">
                            {lowStock.length} Items
                        </span>
                    </div>
                </div>

                {lowStock.length == 0 ? (
                    <div className="p-6 text-sm text-slate-500">
                        No low-stock inventory detected
                    </div>
                ) : (
                    <div className="overflow-auto-x">
                        <table className="min-w-full text-left text-sm">
                            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                                <tr>
                                    <th className="px-6 py-4">Product</th>
                                    <th className="px-6 py-4">Warehouse</th>
                                    <th className="px-6 py-4">Quantity</th>
                                    <th className="px-6 py-4">Threshold</th>
                                    <th className="px-6 py-4">Status</th>
                                </tr>
                            </thead>
                        </table>
                        <tbody className="divide-y divide-slate-100">
                            {lowStock.map((item) => (
                                <tr
                                    key={`${item.product_id}-${item.warehouse_id}`}
                                    className="hover:bg-slate-50"
                                >
                                    <td className="px-6 py-4 font-medium text-slate-900">
                                        {item.product_name}
                                    </td>
                                    <td className="px-6 py-4 text-slate-600">
                                        {item.warehouse_name}
                                    </td>
                                    <td className="px-6 py-4 font-semiboild text-red-600">
                                        {item.quantity}
                                    </td>
                                    <td className="px-6 py-4 text-slate-600">
                                        {item.threshold}
                                    </td>
                                    <td className="px-6 py-4">
                                        <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-700">
                                            Low Stock
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </div>
                )}
            </section>

            {/* Inventory Insights */}
            <section className="rounded-xl border border-slate-200 bg-white shadow-sm">

                <div className="border-b border-slate-200 px-6 py-5">

                    <h2 className="text-lg font-semibold text-slate-900">
                        Inventory Insights
                    </h2>

                    <p className="mt-1 text-sm text-slate-500">
                        Backend-generated inventory recommendations
                    </p>

                </div>

                {insights.length === 0 ? (
                    <div className="p-6 text-sm text-slate-500">
                        No critical inventory insights at this time.
                    </div>
                ) : (
                    <div className="divide-y divide-slate-100">

                        {insights.map((insight) => (
                            <div
                                key={`${insight.product_id}-${insight.warehouse_id}`}
                                className="p-6"
                            >

                                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">

                                    <div>

                                        <div className="flex items-center gap-3">

                                            <h3 className="font-semibold text-slate-900">
                                                {insight.product_name}
                                            </h3>

                                            <span className="rounded-full bg-red-100 px-3 py-1 text-xs font-bold text-red-700">
                                                {insight.severity}
                                            </span>

                                        </div>

                                        <p className="mt-2 text-sm text-slate-500">
                                            {insight.warehouse_name}
                                        </p>

                                    </div>

                                    <div className="text-sm text-slate-600">
                                        Quantity:{" "}
                                        <span className="font-semibold text-red-600">
                                            {insight.quantity}
                                        </span>
                                    </div>

                                </div>

                                <div className="mt-4 rounded-lg bg-red-50 p-4">

                                    <p className="text-sm font-medium text-red-800">
                                        Recommendation
                                    </p>

                                    <p className="mt-1 text-sm text-red-700">
                                        {insight.recommendation}
                                    </p>

                                </div>

                            </div>
                        ))}

                    </div>
                )}

            </section>

        </div>
    )
}

function KpiCard({ title, value }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">

      <p className="text-sm font-medium text-slate-500">
        {title}
      </p>

      <p className="mt-3 whitespace-nowrap text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
        {value}
      </p>

    </div>
  )
}

export default Dashboard