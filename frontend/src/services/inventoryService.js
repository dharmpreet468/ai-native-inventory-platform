import api from "./api"

export const getInventories = async () => {
  const response = await api.get("/inventories/")
  return response.data
}

export const getInventory = async (inventoryId) => {
  const response = await api.get(`/inventories/${inventoryId}`)
  return response.data
}

export const createInventory = async (inventory) => {
  const response = await api.post("/inventories/", inventory)
  return response.data
}

export const updateInventory = async (
  inventoryId,
  inventory
) => {
  const response = await api.put(
    `/inventories/${inventoryId}`,
    inventory
  )

  return response.data
}

export const patchInventory = async (
  inventoryId,
  updates
) => {
  const response = await api.patch(
    `/inventories/${inventoryId}`,
    updates
  )

  return response.data
}

export const deleteInventory = async (inventoryId) => {
  await api.delete(`/inventories/${inventoryId}`)
}