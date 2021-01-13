import axios from 'axios';

import serverUrl from '../mixin/url';

const initialState = {
  products: [],
  inProgress: false,
};

const getters = {
  products: (state) => state.products,
  inProgress: (state) => state.inProgress,
};

const scale = {
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
      state.products = data;
    },
    setInProgress(state, inProgress) {
      state.inProgress = inProgress;
    },
  },
};

export default scale;
