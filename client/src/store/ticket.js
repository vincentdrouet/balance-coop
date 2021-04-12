const initialState = {
  labels: [],
};

const getters = {
  labels: (state) => state.labels,
};

const ticket = {
  namespaced: true,
  state: initialState,
  getters,
  actions: {
    add({ commit }, { label }) {
      commit('addLabel', label);
    },
    reset({ commit }) {
      commit('reset');
    },
  },
  mutations: {
    addLabel(state, label) {
      state.labels.push(label);
    },
    reset(state) {
      state.labels = [];
    },
  },
};

export default ticket;
