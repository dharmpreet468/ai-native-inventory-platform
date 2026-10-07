import api from "./api"

export const getInventorySummary = async()=>{
    const response = await api.get("/analytics/summary")
    return response.data
}

export const getLowStockInventory = async(threshold = 20)=>{
    const response = await api.get("/analytics/low-stock",{
        params:{
            threshold,
        },
    })

    return response.data
}

export const getInventoryInsight = async(threshold=20) =>{
    const response = await api.get("/analytics/inventory-insights",{
        params:{
            threshold,
        },
    })

    return response.data
}