import Vue from 'vue';
import Vuex from 'vuex';
import ticket from './ticket';
import products from './products';
import scale from './scale';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    ticket,
    products,
    scale,
  },
  strict: process.env.NODE_ENV !== 'production',
});
