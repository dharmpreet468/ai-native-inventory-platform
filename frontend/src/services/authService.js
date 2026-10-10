import api from "./api"
import tokenManager from "./tokenManager"

const authService = {
    async login(username, password) {
        const response = await api.post("/auth/login", {
            username,
            password,
        })

        const tokens = response.data

        tokenManager.setAccessToken(tokens.access_token)
        tokenManager.setRefreshToken(tokens.refresh_token)

        return tokens
    },

    async register(username, email, password) {
        const response = await api.post("/auth/register", {
            username,
            email,
            password,
        })

        return response.data
    },

    async getCurrentUser() {
        const response = await api.get("/auth/me")
        return response.data
    },

    async refreshAccessToken() {
        const currentRefreshToken = tokenManager.getRefreshToken()


        if (!currentRefreshToken) {
            throw new Error("No refresh token available")
        }

        const response = await api.post("/auth/refresh", {
            refresh_token: currentRefreshToken,
        })

        const tokens = response.data

        // Save both replacement tokens after rotation.
        tokenManager.setAccessToken(tokens.access_token)
        tokenManager.setRefreshToken(tokens.refresh_token)

        return tokens.access_token
    },

    logout() {
        tokenManager.clearTokens()
    },
}

export default authService