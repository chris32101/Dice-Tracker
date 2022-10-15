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

<script>
import axios from "axios";
import Vue from "vue";

export default {
  components: {
    //Bracket
  },
  data: function () {
    // returned data
    return {
      isOwner: this.getIsOwner(),
      rounds: rounds,
      headers: headers,
      teams: teams,
      leagueName: this.getLeagueName(),
      teamlist: this.getTeamList(), // leagueTeams: this.userArray()
      challongeURL: this.getChallongeURL(),
      allMatches: this.getAllMatches(),
      matchHeaders: [
        { text: "Game #", align: "start", sortable: false, value: "id" },
        {
          text: "Referee Link",
          align: "start",
          sortable: false,
          value: "link",
        },
      ],
      gameDirectLinks: this.generateLinks(),
      refereeLink: this.directLink(),
    };
  },
  
};
//Round of 8
const rounds = [
  {
    games: [
      {
        player1: { id: "1", name: "Competitor 1", winner: false },
        player2: { id: "8", name: "Competitor 4", winner: true },
      },
      {
        player1: { id: "4", name: "Competitor 4", winner: false },
        player2: { id: "5", name: "Competitor 5", winner: true },
      },
      {
        player1: { id: "2", name: "Competitor 2", winner: false },
        player2: { id: "7", name: "Competitor 7", winner: true },
      },
      {
        player1: { id: "3", name: "Competitor 3", winner: false },
        player2: { id: "6", name: "Competitor 6", winner: true },
      },
    ],
  },
  {
    //Semifinals
    games: [
      {
        player1: { id: "8", name: "Competitor 4", winner: false },
        player2: { id: "5", name: "Competitor 5", winner: true },
      },
      {
        player1: { id: "6", name: "Competitor 6", winner: false },
        player2: { id: "7", name: "Competitor 7", winner: true },
      },
    ],
  },
  //Finals
  {
    games: [
      {
        player1: { id: "5", name: "Competitor 5", winner: false },
        player2: { id: "7", name: "Competitor 7", winner: true },
      },
    ],
  },
];
const headers = [
    {
      text: "Team Name",
      align: "start",
      sortable: false,
      value: "name",
    },
    { text: "Shots: #", value: "shots" },
    { text: "Table Hits: #", value: "table_hits" },
    { text: "Points: #", value: "points" },
    { text: "Clinks: #", value: "clinks" },
    { text: "Dunks: #", value: "dunks" },
    { text: "P. Points: #", value: "p_points" },
    { text: "Catches: #", value: "catches" },
    { text: "Drops: #", value: "drops" },
    { text: "Table Hit %: #", value: "table_hit_p" },
    { text: "PP %: #", value: "p_point_p" },
  ],
  // dummy data
  teams = [
    {
      name: "Team 1",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 2",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 3",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 4",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 5",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 6",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 7",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
    {
      name: "Team 8",
      shots: 159,
      table_hits: 145,
      points: 24,
      clinks: 8,
      dunks: 3,
      p_points: 120,
      catches: 106,
      drops: 33,
      table_hit_p: 91,
      p_point_p: 75,
    },
  ];
</script>

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