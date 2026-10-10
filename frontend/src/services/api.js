import axios from "axios"
import tokenManager from "./tokenManager"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL_BASE,
    headers: {
        "Content-Type": "application/json",
    },
})

// Attach the current access token to outgoing requests.
api.interceptors.request.use(
    (config) => {
        const accessToken = tokenManager.getAccessToken()

        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`
        }

        return config
    },
    (error) => Promise.reject(error)
)

let refreshPromise = null

api.interceptors.response.use(
    (response) => response,

    async (error) => {
        const originalRequest = error.config
        const status = error.response?.status

        if (!originalRequest || status !== 401) {
            return Promise.reject(error)
        }

        const requestUrl = originalRequest.url || ""

        // Never refresh after login or refresh itself fails.
        if (
            requestUrl.includes("/auth/login") ||
            requestUrl.includes("/auth/refresh")
        ) {
            return Promise.reject(error)
        }

        // Prevent an infinite retry loop.
        if (originalRequest._retry) {
            return Promise.reject(error)
        }

        originalRequest._retry = true

        try {
            if (!refreshPromise) {
                // Dynamic import avoids a circular dependency.
                refreshPromise = import("./authService")
                    .then(({ default: authService }) =>
                        authService.refreshAccessToken()
                    )
                    .finally(() => {
                        refreshPromise = null
                    })
            }

            const newAccessToken = await refreshPromise

            originalRequest.headers =
                originalRequest.headers || {}

            originalRequest.headers.Authorization =
                `Bearer ${newAccessToken}`

            return api(originalRequest)
        } catch (refreshError) {
            tokenManager.clearTokens()

            window.dispatchEvent(new Event("auth:logout"))

            return Promise.reject(refreshError)
        }
    }
)

export default api