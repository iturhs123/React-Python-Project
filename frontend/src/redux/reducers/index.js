import productReducer from "./productReducer";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
    product: productReducer,
});

export default rootReducer;

// root reducer is used to combine all the reducers in the application. 
// In this case, we only have one reducer, productReducer, but we can add more reducers in the future if needed. 
// The combineReducers function takes an object where the keys are the names of the reducers and the
//  values are the reducer functions themselves. This allows us to access the state of each reducer using its key in the state object.