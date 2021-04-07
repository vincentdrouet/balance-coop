<template>
  <v-col
    class="pa-0 ma-0"
    style="height: 100vh"
  >
    <v-dialog
      v-if="selectedProduct"
      v-model="selectedProduct"
      max-width="50%"
    >
      <Product :product="selectedProduct" selected @cancel="cancelSelection"/>
    </v-dialog>
    <v-container
      v-if="inProgress"
      class="d-flex flex-column justify-center"
      style="height: 100%; width: 100%; align-items: center"
    >
      <h2>La mise à jour des produits peut prendre un certain temps.<br/>Merci de patienter.</h2>
      <v-progress-circular
        indeterminate
        :size="100"
        :width="7"
        color="primary"
      />
    </v-container>
    <v-card v-else-if="bagsOfProducts.length > 0" flat cols="10" style="height: 100%">
      <v-list-item-group
        v-model="selectedProduct"
        color="indigo"
        style="height: 100%"
      >
        <v-card-actions class="justify-space-around" style="height: 10%">
          <v-btn
            depressed
            outlined
            x-large
            @click="prev"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-item-group
            v-model="onBoarding"
            class="text-center d-flex justify-space-around"
            mandatory
            style="width: 100%"
          >
            <v-item
              v-for="n in bagsOfProducts.length"
              :key="`btn-${n}`"
              v-slot="{ active, toggle }"
            >
              <v-btn
                :input-value="active"
                icon
                width="56px"
                height="56px"
                @click="toggle"
              >
                <v-icon :x-large="bagsOfProducts.length<25">
                  mdi-record
                </v-icon>
              </v-btn>
            </v-item>
          </v-item-group>
          <v-btn
            depressed
            outlined
            x-large
            @click="next"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-actions>
        <v-window v-model="onBoarding" style="height: 85%">
          <v-window-item
            v-for="(page, p) in bagsOfProducts"
            :key="`page-${p}`"
            style="height: 100%"
          >
            <v-card
              style="height: 100%"
              class="d-flex flex-column">
              <v-row
                v-for="(row, r) in page"
                :key="`row-${r}`"
                class="pa-0 ma-0"
                :style="`height: ${100/rowsNb}%`"
              >
                <v-col
                  v-for="(product, c) in row"
                  :key="`col-${c}`"
                  class="pa-0 ma-0"
                >
                  <v-list-item
                    v-if="product"
                    class="pa-0 ma-0"
                    style="height: 100%"
                    three-line
                    :value="product">
                    <Product :product="product"/>
                  </v-list-item>
                </v-col>
              </v-row>
            </v-card>
          </v-window-item>
        </v-window>
      </v-list-item-group>
    </v-card>
  </v-col>
</template>

<script>

import Product from './Product.vue';

export default {
  name: 'Products',
  components: {
    Product,
  },
  props: {
    filter: String,
    onlyBio: Boolean,
    productsCategory: String,
  },
  data: () => ({
    selectedProduct: null,
    onBoarding: 0,
    columnsNb: 4,
    rowsNb: 4,
  }),
  watch: {
    productsCategory() {
      this.onBoarding = 0;
    },
  },
  methods: {
    next() {
      if (this.onBoarding + 1 === this.bagsOfProducts.length) {
        this.onBoarding = 0;
      } else {
        this.onBoarding += 1;
      }
    },
    prev() {
      if (this.onBoarding - 1 < 0) {
        this.onBoarding = this.bagsOfProducts.length - 1;
      } else {
        this.onBoarding -= 1;
      }
    },
    cancelSelection() {
      this.$emit('clearFilter');
      this.selectedProduct = null;
    },
  },
  computed: {
    bagsOfProducts() {
      const nbProductsByPage = this.columnsNb * this.rowsNb;
      const nbPages = Math.ceil(this.products.length / nbProductsByPage);
      const bagsOfProducts = new Array(nbPages); // Page / Row / Column
      for (let p = 0; p < bagsOfProducts.length; p += 1) {
        bagsOfProducts[p] = new Array(this.rowsNb);
        for (let r = 0; r < this.rowsNb; r += 1) {
          bagsOfProducts[p][r] = new Array(this.columnsNb);
        }
      }
      this.products.forEach((product, i) => {
        const p = Math.floor(i / nbProductsByPage);
        const r = Math.floor((i % nbProductsByPage) / this.columnsNb);
        const c = i % this.columnsNb;
        bagsOfProducts[p][r][c] = product;
      });
      return bagsOfProducts;
    },
    products() {
      let { products } = this.$store.state.products;
      if (this.filter) {
        products = products.filter((product) => {
          if (String(product.id).startsWith(this.filter)) {
            return true;
          }
          const name = product.name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
          const words = this.filter.toLowerCase().split(' ');
          for (let i = 0; i < words.length; i += 1) {
            const word = words[i];
            if (!name.includes(word.toLowerCase())) {
              return false;
            }
          }
          return true;
        });
      }
      if (this.onlyBio) {
        products = products.filter((product) => product.bio);
      }
      if (this.productsCategory) {
        products = products.filter((product) => product.category === this.productsCategory);
      }
      return products;
    },
    inProgress() {
      return this.$store.state.products.inProgress;
    },
  },
};
</script>

<style>
  .v-list-item {
    width: 20vw;
    height: 20vh;
  }
  .v-window__container {
    height: 100% !important;
  }
</style>
