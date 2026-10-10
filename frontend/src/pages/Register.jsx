import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

export default function Register() {
    const { register } = useAuth()
    const navigate = useNavigate()

    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")

    const [error, setError] = useState("")
    const [success, setSuccess] = useState("")
    const [submitting, setSubmitting] = useState(false)

    async function handleSubmit(event) {
        event.preventDefault()

        setError("")
        setSuccess("")

        if (password !== confirmPassword) {
            setError("Passwords do not match.")
            return
        }

        if (password.length < 8) {
            setError("Password must contain at least 8 characters.")
            return
        }

        setSubmitting(true)

        try {
            await register(username, email, password)

            setSuccess("Registration successful. Redirecting to login...")

            setTimeout(() => {
                navigate("/login", { replace: true })
            }, 1000)
        } catch (err) {
            const status = err.response?.status
            const detail = err.response?.data?.detail

            if (status === 409) {
                setError(
                    typeof detail === "string"
                        ? detail
                        : "Username or email already exists."
                )
            } else if (status === 422) {
                setError(
                    "Invalid registration details. Check your username, email, and password."
                )
            } else {
                setError(
                    "Registration failed. Check your connection and try again."
                )
            }
        } finally {
            setSubmitting(false)
        }
    }

    return (
        <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-8">
            <section className="w-full max-w-md rounded-xl bg-white p-8 shadow-lg">
                <h1 className="mb-2 text-2xl font-bold text-slate-900">
                    Create Account
                </h1>

                <p className="mb-6 text-sm text-slate-600">
                    Register to access the Inventory Platform.
                </p>

                {error && (
                    <div
                        role="alert"
                        className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700"
                    >
                        {error}
                    </div>
                )}

                {success && (
                    <div
                        role="status"
                        className="mb-4 rounded-md bg-green-50 p-3 text-sm text-green-700"
                    >
                        {success}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label
                            htmlFor="username"
                            className="mb-1 block text-sm font-medium text-slate-700"
                        >
                            Username
                        </label>

                        <input
                            id="username"
                            type="text"
                            autoComplete="username"
                            minLength={3}
                            maxLength={100}
                            required
                            value={username}
                            onChange={(event) =>
                                setUsername(event.target.value)
                            }
                            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="email"
                            className="mb-1 block text-sm font-medium text-slate-700"
                        >
                            Email
                        </label>

                        <input
                            id="email"
                            type="email"
                            autoComplete="email"
                            required
                            value={email}
                            onChange={(event) =>
                                setEmail(event.target.value)
                            }
                            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="password"
                            className="mb-1 block text-sm font-medium text-slate-700"
                        >
                            Password
                        </label>

                        <input
                            id="password"
                            type="password"
                            autoComplete="new-password"
                            minLength={8}
                            maxLength={128}
                            required
                            value={password}
                            onChange={(event) =>
                                setPassword(event.target.value)
                            }
                            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="confirmPassword"
                            className="mb-1 block text-sm font-medium text-slate-700"
                        >
                            Confirm Password
                        </label>

                        <input
                            id="confirmPassword"
                            type="password"
                            autoComplete="new-password"
                            required
                            value={confirmPassword}
                            onChange={(event) =>
                                setConfirmPassword(event.target.value)
                            }
                            className="w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={submitting}
                        className="w-full rounded-md bg-blue-600 px-4 py-2 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {submitting ? "Creating Account..." : "Register"}
                    </button>
                </form>

                <p className="mt-5 text-center text-sm text-slate-600">
                    Already have an account?{" "}
                    <Link
                        to="/login"
                        className="font-medium text-blue-600 hover:underline"
                    >
                        Sign in
                    </Link>
                </p>
            </section>
        </main>
    )
}