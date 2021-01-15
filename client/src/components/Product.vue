<template>
  <v-list-item-content class="pa-0 ma-0">
      <v-card>
        <v-card-title>{{ product.name }}</v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              <v-img
                v-if="product.image_medium"
                :src="'data:image/jpeg;base64,'+product.image_medium"
                max-height="140"
                max-width="250"
              />
              <v-img
                v-else
                src="@/assets/logo.png"
                max-height="140"
                max-width="140"
                class="mx-auto"
              />
            </v-col>
            <v-col class="pa-0 ma-0 align-self-center" align="center">
              <h2>{{ asEuro(product.theoritical_price) }} / kg</h2>
              <v-img
                v-if="product.bio"
                src="@/assets/bio.jpeg"
                max-height="50"
                max-width="40"
                class="mt-6"
              />
            </v-col>
            <v-col class="pa-0 ma-0 align-self-center" align="center" v-if="selected">
              <v-row>
                <v-col>
                  <h2 :class="weight>0?'text-right':'orange--text text-right'">
                    Poids :
                  </h2>
                </v-col>
                <v-col>
                  <h2 :class="weight>0?'text-left':'orange--text'">
                    {{ Number((weight).toFixed(3)) }} kg
                  </h2>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <h1 :class="weight>0?'text-right':'orange--text text-right'">
                    Prix :
                  </h1>
                </v-col>
                <v-col>
                  <h1 :class="weight>0?'text-left':'orange--text'">
                    {{ asEuro(product.theoritical_price * weight) }}
                  </h1>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions v-if="selected" class="justify-space-around">
          <v-btn width="200px" height="80px"
                 @click="$emit('cancel')">
            Annuler
          </v-btn>
          <v-btn width="200px" height="80px"
                 @click="weightChange=!weightChange"
                 :input-value="weightChange">
            Modifier le poids
          </v-btn>
          <v-btn width="200px" height="80px"
                 @click="$emit('cancel')"
                 :disabled="weight<=0">
            Valider
          </v-btn>
        </v-card-actions>
        <v-card-actions v-if="selected && weightChange">
          <Keyboard @pressed="pressed"/>
        </v-card-actions>
      </v-card>
  </v-list-item-content>
</template>

<script>

import Keyboard from './Keyboard.vue';

export default {
  name: 'Product',
  props: {
    product: Object,
    selected: Boolean,
  },
  components: {
    Keyboard,
  },
  data: () => ({
    weight: 0.0,
    healthy: false,
    connected: false,
    weightChange: false,
  }),
  created() {
    this.healthy = this.$store.state.scale.healthy;
    this.connected = this.$store.state.scale.connected;
    if (this.healthy && this.connected) {
      this.weight = this.$store.state.scale.weight;
    } else {
      this.weightChange = true;
    }
  },
  methods: {
    asEuro(number) {
      // Create our number formatter.
      const formatter = new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR',
      });
      return formatter.format(number);
    },
    pressed(value) {
      if (value) {
        this.weight = parseFloat(value);
      } else {
        this.weight = 0.0;
      }
    },
  },
};
</script>

<style scoped>
</style>
