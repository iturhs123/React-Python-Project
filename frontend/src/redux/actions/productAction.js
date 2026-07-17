import axios from "axios";


export const fetchProductsRequest = () => {
  return {
    type: "FETCH_PRODUCTS_REQUEST",
  };
}

export const fetchProductsSuccess = (products) => {
  return {
    type: "FETCH_PRODUCTS_SUCCESS",
    payload: products,
  };
}

export const fetchProductsFailure = (error) => {
  return {
    type: "FETCH_PRODUCTS_FAILURE",
    payload: error,
  };
}
export const setLoading = (loading) => ({
  type: "SET_LOADING",
  payload: loading,
});

export const setError = (error) => ({
  type: "SET_ERROR",
  payload: error,
});

export const clearError = () => ({
  type: "CLEAR_ERROR",
});
// todo
// ADD_PRODUCT_SUCCESS 
// UPDATE_PRODUCT_SUCCESS
// DELETE_PRODUCT_SUCCESS

export const fetchProducts = () => {
  return async (dispatch, getState) => {
    dispatch(fetchProductsRequest());
    try {
      const response = await axios.get("http://localhost:8000/products",);
      console.log("Fetched products:", response.data); // Log the fetched products
      dispatch(fetchProductsSuccess(response.data));
    } catch (error) {
      dispatch(fetchProductsFailure(error.message));
    }finally {
      dispatch(setLoading(false));
    }
  }
}

export const addProducts = (product) => {
  return async (dispatch, getState) => {
     console.log("INSIDE THUNK");
    dispatch(setLoading(true));
    dispatch(clearError());
    try {
    console.log("Before axios");
      const response = await axios.post("http://localhost:8000/products", {
        ...product,
        id: Number(product.id),
        price: Number(product.price),
        quantity: Number(product.quantity),
      });
          console.log("After axios");
      dispatch(fetchProducts());
      dispatch(setLoading(false));
      return response.data;
    } catch (error) {
      dispatch(setLoading(false));

      dispatch(
        setError(
          error.response?.data?.detail ||
          error.message ||
          "Failed to add product"
        )
      );
    }
  }
}


export const updateProducts = (id, product) => {
  return async (dispatch, getState) => {
 dispatch(setLoading(true));
     try {
      const response = await axios.put(`http://localhost:8000/products/${id}`, {
        ...product,
        id: Number(product.id),
        price: Number(product.price),
        quantity: Number(product.quantity),
      });
      dispatch(fetchProductsSuccess(response.data));
    } 
    catch (err) {
      dispatch(
        fetchProductsFailure(
          err.response?.data?.detail ||
          err.message
        )
      );
    } finally {
      dispatch(setLoading(false));
    }
  }
}




//thunk ann action creator that returns a function instead of plain object.
// redux-thunk middleware lets the store dispatch functions, givin it access to "dispatch" and "getstate". 