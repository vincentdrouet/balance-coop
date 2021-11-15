import axios from 'axios';

import serverUrl from '../mixin/url';

const initialState = {
  synced: false,
  date: '',
  products: [],
  inProgress: false,
};

const getters = {
  products: (state) => state.products,
  inProgress: (state) => state.inProgress,
};

const products = {
  namespaced: true,
  state: initialState,
  getters,
  actions: {
    get({ commit }) {
      return new Promise((resolve, reject) => {
        commit('setInProgress', true);
        axios.get(
          `${serverUrl()}/products`,
        ).then(({ data }) => {
          commit('setProducts', data);
          resolve(data);
          commit('setInProgress', false);
        }).catch((error) => {
          reject(error);
          commit('setInProgress', false);
        });
      });
    },
  },
  mutations: {
    setProducts(state, data) {
      state.synced = data.synced;
      state.date = data.date;
      state.products = data.products;
    },
    setInProgress(state, inProgress) {
      state.inProgress = inProgress;
    },
  },
};

export default products;
