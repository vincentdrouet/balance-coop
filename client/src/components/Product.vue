<template>
  <v-list-item-content class="pa-0 ma-0">
    <v-dialog
      v-model="printError"
      width="500"
    >
      <v-card class="text-center">
        <v-card-title class="headline red lighten-2" style="justify-content: center">
          Erreur d'impression !
        </v-card-title>

        <v-card-text class="pa-3 ma-0">
          Il semble impossible d'imprimer le ticket.<br/>
          Verifier la mise sous tention et le cablage de l'imprimante.<br/>
          Si le problème perciste, contacter le groupe informatique.<br/>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="printError = false"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-card>
      <v-card-title class="pb-1 pr-0">
        <h4>{{ product.name }}</h4>
      </v-card-title>
      <v-card-text class="pa-0 ma-0">
        <v-row class="pa-0 ma-0 pr-4">
          <v-col class="pa-0 ma-0 pl-4">
            <v-img
              v-if="product.image_medium"
              :src="'data:image/jpeg;base64,'+product.image_medium"
              :aspect-ratio="4/3"
              height="90%"
            />
            <v-img
              v-else
              src="@/assets/logo.png"
              :aspect-ratio="4/3"
              height="100%"
              class="mx-auto"
            />
          </v-col>
          <v-col
            class="pa-0 ma-0 d-flex flex-column justify-start align-center"
            style="height: 100%"
          >
            <h2>Id. {{ product.id }}</h2>
            <h2><br/>{{ asEuro(product.theoritical_price) }} / kg</h2>
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
                <h2 :class="weight>0&&weight<100?'text-right':'orange--text text-right'">
                  Poids :
                </h2>
              </v-col>
              <v-col>
                <h2 :class="weight>0&&weight<100?'text-left':'orange--text'">
                  {{ Number((weight).toFixed(3)) }} kg
                </h2>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <h2 :class="weight>0&&weight<100?'text-right':'orange--text text-right'">
                  Prix * :
                </h2>
              </v-col>
              <v-col>
                <h2 :class="weight>0&&weight<100?'text-left':'orange--text'">
                  {{ asEuro(product.theoritical_price * weight) }}
                </h2>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions v-if="printInProgress && selected"  class="justify-center">
        <v-progress-circular
          indeterminate
          :size="100"
          :width="7"
          color="primary"
          v-if="printInProgress && selected"
        />
      </v-card-actions>
      <v-card-actions v-else-if="selected" class="justify-space-around">
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
               @click="printLabel(false)"
               :disabled="weight<=0 || weight>=100">
          Valider
        </v-btn>
        <v-btn width="200px" height="80px"
               @click="printLabel(true)"
               :disabled="weight<=0 || weight>=100">
          Valider<br/>et<br/>Couper le ticket
        </v-btn>
      </v-card-actions>
      <v-card-actions v-if="selected && weightChange">
        <Keyboard @pressed="pressed" onlyNum/>
      </v-card-actions>
      <v-card-text v-if="selected" class="pr-0">
        <h4>
          * Le prix est donné à titre indicatif. Le calcul se fera en caisse au regard du poid.
        </h4>
      </v-card-text>
    </v-card>
  </v-list-item-content>
</template>

<script>

import Keyboard from './Keyboard.vue';
import print from '../mixin/print';

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
    weightChange: false,
    printInProgress: false,
    printError: '',
  }),
  created() {
    if (!this.healthy || !this.connected) {
      this.weightChange = true;
      this.weight = 0.0;
    } else {
      this.weight = this.weightFromScale;
    }
  },
  watch: {
    weightChange() {
      if (!this.weightChange) {
        this.weight = this.weightFromScale;
      }
    },
    weightFromScale() {
      if (!this.weightChange) {
        this.weight = this.weightFromScale;
      }
    },
    healthy() {
      if (!this.healthy || !this.connected) {
        this.weightChange = true;
        this.weight = 0.0;
      }
    },
    connected() {
      if (!this.healthy || !this.connected) {
        this.weightChange = true;
        this.weight = 0.0;
      }
    },
  },
  computed: {
    weightFromScale() {
      return this.$store.state.scale.weight;
    },
    healthy() {
      return this.$store.state.scale.healthy;
    },
    connected() {
      return this.$store.state.scale.connected;
    },
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
    printLabel(cut) {
      this.printInProgress = true;
      print(
        this.product,
        this.weight,
        cut,
      ).then(() => {
        this.printInProgress = false;
        this.$emit('cancel');
      }).catch(() => {
        this.printInProgress = false;
        this.printError = true;
      });
    },
  },
};
</script>

<style scoped>
</style>
