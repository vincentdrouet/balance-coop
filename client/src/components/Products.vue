<template>
  <v-col>
    <v-dialog
      v-if="selectedProduct"
      v-model="selectedProduct"
      max-width="50%"
    >
      <Product :product="selectedProduct" selected @cancel="cancelSelection"/>
    </v-dialog>
    <v-container
      v-if="inProgress"
      class="d-flex flex-column align-self-center">
      <h2>La mise à jour des produits peut prendre un certain temps.<br/>Merci de patienter.</h2>
      <v-progress-circular
        indeterminate
        :size="100"
        :width="7"
        color="primary"
      />
    </v-container>
    <v-card v-else-if="bagsOfProducts.length > 0" flat cols="10">
      <v-list-item-group
        v-model="selectedProduct"
        color="indigo"
      >
        <v-card-actions class="justify-space-between">
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
            class="text-center"
            mandatory
          >
            <v-item
              v-for="n in bagsOfProducts.length"
              :key="`btn-${n}`"
              v-slot="{ active, toggle }"
            >
              <v-btn
                :input-value="active"
                icon
                x-large
                @click="toggle"
              >
                <v-icon>mdi-record</v-icon>
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
        <v-window v-model="onBoarding">
          <v-window-item
            v-for="(page, p) in bagsOfProducts"
            :key="`page-${p}`"
          >
            <v-card>
              <v-row
                v-for="(row, r) in page"
                :key="`row-${r}`"
              >
                <v-col
                  v-for="(product, c) in row"
                  :key="`col-${c}`"
                >
                  <v-list-item v-if="product" class="pa-0 ma-0" three-line :value="product">
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
    productsCategory: String,
  },
  data: () => ({
    selectedProduct: null,
    onBoarding: 0,
    rowsNb: 4,
    columnsNb: 3,
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
      if (this.productsCategory) {
        return this.$store.state.products.products.filter(
          (product) => product.categ === this.productsCategory,
        );
      }
      return this.$store.state.products.products;
    },
    inProgress() {
      return this.$store.state.products.inProgress;
    },
  },
};
</script>

<style scoped>
  .v-list-item {
    width: 25vw;
    height: 20vh;
  }
</style>
