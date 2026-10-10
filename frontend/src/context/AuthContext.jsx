import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react"

import authService from "../services/authService"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    const [refreshToken, setRefreshToken] = useState(null)

    useEffect(() => {
        let active = true

        async function restoreSession() {
            const accessToken = sessionStorage.getItem("access_token")

            if (!accessToken) {
                setLoading(false)
                return
            }

            try {
                const currentUser = await authService.getCurrentUser()

                if (active) {
                    setUser(currentUser)
                }
            } catch {
                if (active) {
                    sessionStorage.removeItem("access_token")
                    setUser(null)
                }
            } finally {
                if (active) {
                    setLoading(false)
                }
            }
        }

        restoreSession()

        return () => {
            active = false
        }
    }, [])

    useEffect(() => {
        function handleLogout() {
            setUser(null)
            setRefreshToken(null)
        }

        window.addEventListener("auth:logout", handleLogout)

        return () => {
            window.removeEventListener(
                "auth:logout",
                handleLogout
            )
        }
    }, [])

    async function login(username, password) {
        const tokens = await authService.login(username, password)

        try {
            const currentUser = await authService.getCurrentUser()

            setUser(currentUser)

            return currentUser
        } catch (error) {
            authService.logout()
            setUser(null)

            throw error
        }
    }

    async function register(username, email, password) {
        return authService.register(username, email, password)
    }

    async function refreshAccessToken() {
        if (!refreshToken) {
            throw new Error("No refresh token is available")
        }

        const tokens = await authService.refreshToken(refreshToken)

        setRefreshToken(tokens.refresh_token)

        return tokens.access_token
    }

    function logout() {
        authService.logout()
        setUser(null)
    }

    const value = {
        user,
        loading,
        isAuthenticated: Boolean(user),
        login,
        register,
        logout,
        refreshAccessToken,
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )

}

export function useAuth() {
    const context = useContext(AuthContext)

    if (!context) {
        throw new Error("useAuth must be used within an AuthProvider")
    }

    return context
}