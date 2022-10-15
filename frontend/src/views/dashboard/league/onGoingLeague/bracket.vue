<template>
  <div class="home">
    <v-container>
      <v-row>
        <div class="hero">
          <h2>{{ leagueName }} Bracket</h2>
          <br />
          <iframe
            class="bracketframe"
            :src="challongeURL"
            width="1140"
            height="500"
            frameborder="1"
            scrolling="auto"
            allowtransparency="true"
          ></iframe>
        </div>
      </v-row>
    </v-container>
    <v-container>
      <v-row> </v-row>
    </v-container>
    <v-container v-if="isOwner == true">
      <v-row>
        <v-btn small color="success" v-on:click="refreshPage()"
          >Refresh matches</v-btn
        >
      </v-row>
      <v-row>
        <h4>
          Listed below are direct links to referee each of the games above!
        </h4>
        <br />
      </v-row>
      <v-row>
        <br />
        <h4><a :href="refereeLink">Match #1</a></h4>
        <br />
        <v-data-table
          dense
          :headers="matchHeaders"
          :items="gameDirectLinks"
          item-key="name"
          class="elevation-1"
        >
        </v-data-table>
      </v-row>
    </v-container>
  </div>
</template>



<style scoped>
video {
  object-fit: cover !important;
  width: 100vw;
  height: 100vh;
  position: fixed;
  left: 0;
}
.headerSnappa {
  color: black;
  text-align: center;
  position: absolute;
  left: 60%;
  top: 25%;
  transform: translate(-50%, 0%);
  font-size: 8vh;
}

.bracketcard {
  left: 0%;
  color: white;
}
.bracketframe {
  border-radius: 20px;
  border-width: 20px;
  border-color: #2b344d;
  border-style: solid;
}
</style>