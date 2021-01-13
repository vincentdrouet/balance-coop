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
            >
              <v-spacer></v-spacer>
              <v-row>
                <v-btn value="fruit" width="150px" height="80px">Fruits</v-btn>
                <v-btn value="legume" width="150px" height="80px">Légumes</v-btn>
              </v-row>
              <v-row>
                <v-btn value="vrac" width="150px" height="80px">Vrac</v-btn>
              </v-row>
              <v-row>
                <v-btn value="viande" width="150px" height="80px">Viande</v-btn>
                <v-btn value="poisson" width="150px" height="80px">Poisson</v-btn>
              </v-row>
              <v-row>
                <v-btn value="fruit_sec" width="150px" height="80px">Fruits secs</v-btn>
              </v-row>
              <v-row>
                <v-btn value="autre" width="150px" height="80px">Autres</v-btn>
              </v-row>
            </v-container>
          </v-btn-toggle>
        </v-row>
        <v-row no-gutters class="refresh-row flex-column">
          <v-divider class="white"></v-divider>
          <v-spacer></v-spacer>
          <v-btn
            @click="refreshProducts"
            class="align-self-center"
          >Rafraichir les produits</v-btn>
          <v-spacer></v-spacer>
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
