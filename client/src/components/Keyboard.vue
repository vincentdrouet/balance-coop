<template>
  <v-container class="d-flex flex-column grey lighten-5 align-center">
    <v-row no-gutters>
      <h2 :class="isValid()?'pb-5':'red--text pb-5'"> {{ getValue() }}</h2>
    </v-row>
    <v-row
      v-for="r in 3"
      :key="`row_${r}`"
      no-gutters>
      <v-col
        v-for="c in 3"
        :key="`row_${r}-col_${c}`"
      >
        <v-btn width="100px" height="80px" @click="press((r-1)*3+c)">{{ (r-1)*3+c }}</v-btn>
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col
        v-for="c in ['c', '0', '.']"
        :key="`row_4-col_${c}`"
      >
        <v-btn width="100px" height="80px" @click="press(c)">{{ c }}</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  props: ['selfValue'],
  data() {
    return {
      value: '',
    };
  },
  methods: {
    press(key) {
      if (key === 'c') {
        this.value = '';
      } else {
        if (!this.value && key === '.') {
          this.value = '0';
        }
        this.value = `${this.value}${key}`;
      }
    },
    isValid() {
      if (!this.value) {
        return true;
      }
      // eslint-disable-next-line no-restricted-globals
      if (isNaN(Number(this.value))) {
        return false;
      }
      return parseFloat(this.value) > 0;
    },
    getValue() {
      if (!this.value) {
        return '0';
      }
      return this.value;
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
