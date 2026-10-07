import api from "./api"

export const getProducts = async()=>{
    const response = await api.get("/products/")
    return response.data
}

export const getProduct = async(productId)=>{
    const response = await api.get(`/products/${productId}`)
    return response.data
}

export const createProduct = async(product)=>{
    const response = await api.post("/products/",product)
    return response.data
}

export const updateProduct = async(productId, product)=>{
    const response = await api.put(`/products/${productId}`, product)
    return response.data
}

export const patchProduct = async(productId,updates)=>{
    const response = await api.patch(`/products/${productId}`,updates)
    return response.data
}

export const deleteProduct = async(productId)=>{
    await api.delete(`/products/${productId}`)
}

