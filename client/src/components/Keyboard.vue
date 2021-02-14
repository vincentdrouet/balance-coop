<template>
  <v-container class="d-flex flex-column grey lighten-5 align-center">
    <v-row no-gutters style="height: 50px">
      <h2 :class="isValid()?'pb-5':'red--text pb-5'"> {{ getValue() }}</h2>
    </v-row>
    <v-row
      v-for="r in getKeys()"
      :key="`row_${r}`"
      no-gutters>
      <v-col
        v-for="c in r"
        :key="`row_${r}-col_${c}`"
      >
        <v-btn width="100px" height="80px" @click="press(c)">
          <v-icon v-if="c==='SUPPR'">mdi-backspace</v-icon>
          <p v-else>{{ c }}</p>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  props: {
    onlyNum: Boolean,
  },
  data() {
    return {
      value: '',
    };
  },
  methods: {
    press(key) {
      if (key === 'SUPPR') {
        if (this.value) {
          this.value = this.value.slice(0, -1);
        }
      } else {
        if (this.onlyNum && !this.value && key === '.') {
          this.value = '0';
        }
        this.value = `${this.value}${key}`;
        this.value = this.value.trim();
      }
    },
    isValid() {
      if (!this.value) {
        return true;
      }
      if (this.onlyNum) {
        // eslint-disable-next-line no-restricted-globals
        if (isNaN(Number(this.value))) {
          return false;
        }
        return parseFloat(this.value) > 0;
      }
      return true;
    },
    getKeys() {
      if (this.onlyNum) {
        return [
          ['7', '8', '9'],
          ['4', '5', '6'],
          ['1', '2', '3'],
          ['SUPPR', '0', '.'],
        ];
      }
      return [
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
        ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M'],
        ['W', 'X', 'C', 'V', 'B', 'N', 'SUPPR'],
      ];
    },
    getValue() {
      if (!this.value) {
        return this.defaultValue();
      }
      return this.value;
    },
    defaultValue() {
      return this.onlyNum ? '0' : ' ';
    },
    resetValue() {
      this.value = this.defaultValue();
    },
  },
  watch: {
    value() {
      this.$emit('pressed', this.isValid() ? this.value : 0);
    },
  },
};
</script>

<style scoped>
</style>
