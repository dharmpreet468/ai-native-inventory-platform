import api from "./api"

export const getWarehouses = async () => {
  const response = await api.get("/warehouses/")
  return response.data
}

export const getWarehouse = async (warehouseId) => {
  const response = await api.get(`/warehouses/${warehouseId}`)
  return response.data
}

export const createWarehouse = async (warehouse) => {
  const response = await api.post("/warehouses/", warehouse)
  return response.data
}

export const updateWarehouse = async (warehouseId, warehouse) => {
  const response = await api.put(
    `/warehouses/${warehouseId}`,
    warehouse
  )

  return response.data
}

export const patchWarehouse = async (warehouseId, updates) => {
  const response = await api.patch(
    `/warehouses/${warehouseId}`,
    updates
  )

  return response.data
}

export const deleteWarehouse = async (warehouseId) => {
  await api.delete(`/warehouses/${warehouseId}`)
}