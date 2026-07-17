import { createStore, applyMiddleware } from "redux";
import { thunk } from "redux-thunk";
import rootReducer from "./reducers";

const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

export default store;

// steps to use thunk-
// 1. Install redux-thunk using npm or yarn.
// 2. Import thunk from redux-thunk and apply it as middleware when creating the store.
// 3. Create action creators that return functions instead of plain objects. These functions can perform asynchronous operations and dispatch actions based on the results of those operations.
// 4. Use the action creators in your components to dispatch actions and update the state.
