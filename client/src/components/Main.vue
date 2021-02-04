<template>
  <v-container fluid>
    <v-row>
      <v-col cols="2" class="primary d-flex flex-column justify-space-around full-height pa-0 ma-0">
        <v-row no-gutters class="scale-row d-flex">
          <Scale :freeze="freeze"/>
        </v-row>
        <v-row no-gutters>
          <v-btn-toggle
            v-model="productsCategory"
            color="deep-purple accent-3"
            class="filters"
            tile
            group>
            <v-container
              class="filters d-flex flex-column pa-0 ma-0 justify-space-around"
              width="100%"
            >
              <v-row style="width: 100%; justify-content: center" align-content="center">
                <v-btn value="fruit" width="45%" height="80px">Fruits</v-btn>
                <v-btn value="legume" width="45%" height="80px">Légumes</v-btn>
              </v-row>
              <v-row style="width: 100%; justify-content: center" align-content="center">
                <v-btn value="vrac" width="50%" height="80px">Vrac</v-btn>
              </v-row>
              <v-row style="width: 100%; justify-content: center" align-content="center">
                <v-btn value="viande" width="45%" height="80px">Viande</v-btn>
                <v-btn value="poisson" width="45%" height="80px">Poisson</v-btn>
              </v-row>
              <v-row style="width: 100%; justify-content: center" align-content="center">
                <v-btn value="fruit_sec" width="50%" height="80px">Fruits secs</v-btn>
              </v-row>
              <v-row style="width: 100%; justify-content: center" align-content="center">
                <v-btn value="autre" width="50%" height="80px">Autres</v-btn>
              </v-row>
            </v-container>
          </v-btn-toggle>
        </v-row>
        <v-row no-gutters class="refresh-row flex-column" align-content="center">
          <v-divider class="white" width="100%"></v-divider>
          <v-btn
            @click="refreshProducts"
            class="align-self-center"
            style="height: 50%; margin-top: 8%"
          >Rafraichir les produits</v-btn>
        </v-row>
      </v-col>
      <Products :productsCategory="productsCategory"/>
    </v-row>
  </v-container>
</template>

<script>
import Products from './Products.vue';
import Scale from './Scale.vue';

export default {
  name: 'Main',
  components: {
    Products,
    Scale,
  },
  data: () => ({
    productsCategory: null,
    filter: null,
    freeze: false,
  }),
  created() {
    this.refreshProducts();
  },
  methods: {
    refreshProducts() {
      this.$store.dispatch('products/get');
    },
  },
};
</script>

<style scoped>
  .full-height {
    height: 100vh;
  }
  .scale-row {
    max-height: 20%;
  }
  .refresh-row {
    max-height: 10%;
  }
  .filters {
    height: 100%;
    width: 100%;
    align-items: center;
  }
</style>
