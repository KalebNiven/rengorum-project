import { combineReducers } from 'redux';
import auth from './auth';
import modal from './modal';
import register from './register';
import userProfile from './userprofile';
import home from './home';

const rootReducer = combineReducers({
  auth,
  modal,
  register,
  userProfile,
  home
});

export default rootReducer;
