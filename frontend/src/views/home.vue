<template>
  <div class="home">
    <v-container>
      <v-row>
        <div class="hero">
          <div class="backgroundPicture"></div>
          <h1 class="headerDiceTracker">Dice Tracker</h1>
        </div>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {},
};
</script>

<style scoped>
.headerDiceTracker {
  color: black;
  text-align: center;
  position: absolute;
  left: 50%;
  top: 25%;
  transform: translate(-50%, 0%);
  font-size: 8vh;
}
</style>