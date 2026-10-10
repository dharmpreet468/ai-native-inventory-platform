import { NavLink, Outlet, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

const navigation = [
    { name: "Dashboard", path: "/" },
    { name: "Products", path: "/products" },
    { name: "Warehouses", path: "/warehouses" },
    { name: "Inventory", path: "/inventory" },
    { name: "Orders", path: "/orders" },
    { name: "Analytics", path: "/analytics" },
]

function AppLayout() {
    const { user, logout } = useAuth()
    const navigate = useNavigate()

    const isAdmin = user?.role === "admin"

    function handleLogout() {
        logout()
        navigate("/login", { replace: true })
    }

    return (
        <div className="flex min-h-screen bg-slate-100">
            {/* Sidebar */}
            <aside className="flex w-64 shrink-0 flex-col bg-slate-900 text-white">
                {/* Brand */}
                <div className="border-b border-slate-700 p-6">
                    <h1 className="text-lg font-bold">
                        Inventory Platform
                    </h1>

                    <p className="mt-1 text-xs text-slate-400">
                        AI Native Operations
                    </p>
                </div>

                {/* Navbar */}
                <nav className="flex-1 px-4 py-5">
                    <div className="flex flex-col gap-2">
                        {navigation.map((item) => (
                            <NavLink
                                key={item.path}
                                to={item.path}
                                end={item.path === "/"}
                                className={({ isActive }) =>
                                    `block w-full rounded-lg px-4 py-3 text-sm transition ${
                                        isActive
                                            ? "bg-blue-600 text-white"
                                            : "text-slate-300 hover:bg-slate-800 hover:text-white"
                                    }`
                                }
                            >
                                {item.name}
                            </NavLink>
                        ))}
                    </div>
                </nav>

                {/* User information */}
                <div className="border-t border-slate-700 p-5">
                    <p className="truncate text-sm font-semibold">
                        {user?.username ?? "User"}
                    </p>

                    <p className="mt-1 text-xs capitalize text-slate-400">
                        {user?.role ?? "Unknown role"}
                    </p>
                </div>
            </aside>

            {/* Main Application */}
            <div className="flex min-w-0 flex-1 flex-col">
                {/* Top Navbar */}
                <header className="border-b bg-white px-8 py-4">
                    <div className="flex items-center justify-between gap-4">
                        <div>
                            <h2 className="text-lg font-semibold text-slate-900">
                                Inventory Management
                            </h2>

                            <p className="text-sm text-slate-500">
                                Operations Control Center
                            </p>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-600">
                                {isAdmin ? "Administrator" : user?.role ?? "User"}
                            </div>

                            <button
                                type="button"
                                onClick={handleLogout}
                                className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </header>

                {/* Page Content */}
                <main className="flex-1 p-8">
                    <Outlet />
                </main>
            </div>
        </div>
    )
}

export default AppLayout