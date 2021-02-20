<template>
  <v-container fluid>
    <v-row>
      <v-col
        cols="2"
        class="primary d-flex flex-column justify-space-around pa-0 ma-0"
        style="height: 100vh"
      >
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
              <v-row v-for="category in categories"
                     :key="category"
                     style="width: 100%; justify-content: center"
                     align-content="center"
              >
                <v-btn :value="category" width="50%" height="80px">{{ category }}</v-btn>
              </v-row>
              <v-row style="width: 100%; justify-content: center; align-content: center">
                <v-checkbox
                  width="100%"
                  dark
                  class="pa-4"
                  v-model="onlyBio"
                  hide-details
                  label="Uniquement les produits BIO"
                ></v-checkbox>
                <v-checkbox
                  width="100%"
                  dark
                  class="pa-4"
                  v-model="withSomeQty"
                  hide-details
                  label="Uniquement avec stock > 0"
                ></v-checkbox>
              </v-row>
            </v-container>
          </v-btn-toggle>
        </v-row>
        <v-row class="refresh-row d-flex flex-row justify-space-around"
               no-gutters>
          <v-btn
            @click="printLabel"
            fab
          >
            <v-icon>
              mdi-scissors-cutting
            </v-icon>
          </v-btn>
          <v-menu
            top
            :offset-x="true"
            :offset-y="true"
            class="white"
            v-bind:close-on-content-click="false"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                fab
                @click="clearFilter"
              >
                <v-icon>
                  mdi-magnify
                </v-icon>
              </v-btn>
            </template>

            <v-container class="pa-0 ma-0">
              <v-row class="pa-0 ma-0" align="center">
                <Keyboard ref="keyboard" @pressed="pressed"/>
              </v-row>
            </v-container>
          </v-menu>
          <v-menu
            top
            :offset-x="true"
            :offset-y="true"
            class="white"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                v-bind="attrs"
                v-on="on"
                fab
              >
                <v-icon>
                  mdi-wrench
                </v-icon>
              </v-btn>
            </template>

            <v-container
              style="height: 100%; background-color: white"
            >
              <v-row class="pa-0 ma-0" align="center">
                <v-btn
                  @click="refreshProducts"
                  height="80px"
                  width="100%"
                >
                  <v-icon>
                    mdi-refresh
                  </v-icon>
                  Rafraichir les produits
                </v-btn>
              </v-row>
            </v-container>
          </v-menu>
        </v-row>
      </v-col>
      <Products
        :filter="filter"
        :productsCategory="productsCategory"
        :withSomeQty="withSomeQty"
        :onlyBio="onlyBio"
        @clearFilter="clearFilter"
      />
    </v-row>
  </v-container>
</template>

<script>
import Keyboard from './Keyboard.vue';
import Products from './Products.vue';
import Scale from './Scale.vue';
import print from '../mixin/print';

export default {
  name: 'Main',
  components: {
    Keyboard,
    Products,
    Scale,
  },
  data: () => ({
    productsCategory: null,
    withSomeQty: false,
    onlyBio: false,
    filter: null,
    freeze: false,
  }),
  created() {
    this.refreshProducts();
  },
  watch: {
    productsCategory() {
      if (this.productsCategory) {
        this.filter = null;
      }
    },
  },
  computed: {
    categories() {
      const categories = [];
      let addOther = false;
      this.$store.state.products.products.forEach((product) => {
        const { category } = product;
        if (category === 'autre') {
          addOther = true;
        } else if (categories.indexOf(category) < 0) {
          categories.push(category);
        }
      });
      if (addOther) {
        categories.push('autre');
      }
      return categories;
    },
  },
  methods: {
    refreshProducts() {
      this.$store.dispatch('products/get');
    },
    printLabel() {
      print(
        null,
        null,
        true,
      );
    },
    pressed(value) {
      if (value) {
        this.productsCategory = null;
        this.filter = value;
      } else {
        this.filter = null;
      }
    },
    clearFilter() {
      if (this.$refs.keyboard) {
        this.$refs.keyboard.resetValue();
      }
      this.filter = null;
    },
  },
};
</script>

<style scoped>
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
  .theme--light.v-btn--active::before {
    opacity: 0.4;
  }
</style>
