import api from "./api"

export const getOrders = async () => {
  const response = await api.get("/orders/")
  return response.data
}

export const getOrder = async (orderId) => {
  const response = await api.get(`/orders/${orderId}`)
  return response.data
}

export const createOrder = async (order) => {
  const response = await api.post("/orders/", order)
  return response.data
}

export const updateOrder = async (orderId, order) => {
  const response = await api.put(
    `/orders/${orderId}`,
    order
  )

  return response.data
}

export const patchOrder = async (orderId, updates) => {
  const response = await api.patch(
    `/orders/${orderId}`,
    updates
  )

  return response.data
}

export const cancelOrder = async (orderId) => {
  const response = await api.delete(`/orders/${orderId}`)
  return response.data
}