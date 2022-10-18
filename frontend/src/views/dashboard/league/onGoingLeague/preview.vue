<template>
    <div class="Preview">
      <br>
      <br>
      <v-card class="mx-auto" max-width="40%" height="100%">
        <v-card-title class="white--text orange darken-4">Participant List</v-card-title>

        <v-card-text class="pt-4">
        <b>Listed below are all of the pending users for {{ leagueName }} league!</b>
        </v-card-text>

        <v-divider></v-divider>

        <v-virtual-scroll :items="usernames" :item-height="60">
          <template v-slot:default="{ item }">
            <v-list-item>
              <v-list-item-avatar>
                <v-icon>mdi-account</v-icon>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{item}}</v-list-item-title>
              </v-list-item-content>
              <div v-if="isOwner == true">
                <v-list-item-action>
                  <v-btn href="google.com" depressed text>
                    User Stats
                    <v-icon color="orange darken-4" right>
                      mdi-open-in-new
                    </v-icon>
                  </v-btn>
                </v-list-item-action>
                <v-list-item-action>
                  <v-btn href="google.com" depressed text>
                    Kick User
                    <v-icon color="orange darken-4" right>
                      mdi-close
                    </v-icon>
                  </v-btn>
                </v-list-item-action>
              </div>
              <div v-else>
                <v-list-item-action>
                  <v-btn href="google.com" depressed text>
                    User Stats
                    <v-icon color="orange darken-4" right>
                      mdi-open-in-new
                    </v-icon>
                  </v-btn>
                </v-list-item-action>
              </div>
              </v-list-item>
          </template>
        </v-virtual-scroll>
        <div v-if="isOwner == true">
          <center><v-btn id="submitLeague" @click="submitLeague()">Submit League</v-btn><span>&nbsp; &nbsp;</span><v-btn id="deleteLeague" @click="deleteLeague()">Delete League</v-btn></center>
        </div>
        <div v-else>
          <center><v-btn id="confetti" @click="confetti()" text>🎉</v-btn></center>
        </div>
      </v-card>
    </div>
</template>

<style scoped>
.rtl {
  direction: rtl;
}
</style>

<script>
import axios from 'axios';
import Vue from 'vue';
export default {
    data() {
      return {
        teamLength: 0,
        items: this.extractUsers(),
        disabledItems: [],
        map: new Map(),
        teamMap: new Map(),
    }},
    methods:{
        // Deletes a league using an endpoint
        deleteLeague() {
        axios.post("http://127.0.0.1:8000/deleteLeague/", {
            username: localStorage.getItem('username'),
        }, {headers: {'Content-Type': 'application/json'}}).then(function (response) {
            if (response.data.response == false){
                Vue.notify({
                    position: "top center",
                    group: "server",
                    text: response.data.error,
                    type: "error",
                })
                window.location.href = "http://localhost:8080/dashboard/home"
                return(undefined);
            }else{
                Vue.notify({
                    position: "top center",
                    group: "server",
                    text: response.data.error,
                    type: "success",
                })
                window.setTimeout(function () {
                    var leagueName = response.data.leagueName
                    localStorage.setItem('leagueName', leagueName)
                    window.location.href = "http://localhost:8080/dashboard/home"
                }, 300)
                return(undefined);
            }
        })
      },
      // Updates the teams map with their name using their id
        updateTeams(id, teamName) {
            var teamList = this.teamMap.get(id)
            teamList[0] = teamName
            this.teamMap.set(id, teamList)
        },
        // Checks if the array has any duplicates
        hasDuplicates(array) {
            return (new Set(array)).size !== array.length;
        },
        finalizeTeams() {
            var teamNames = []
            for (var x = 0; x < JSON.parse(localStorage.getItem("teamLength")); x++){
                var listofItems = this.teamMap.get(x)
                teamNames.push(listofItems[0])
                if (listofItems[0] == "" || listofItems[1] == "" || listofItems[2] == ""){
                    Vue.notify({
                        position: "top center",
                        group: "server",
                        text: "All teams need to be filled before starting games!",
                        type: "error",
                    })
                    return(undefined);
                }
            }
            if (this.hasDuplicates(teamNames)){
                Vue.notify({
                    position: "top center",
                    group: "server",
                    text: "Duplicate team names are not allowed!",
                    type: "error",
                })
                return(undefined);
            }
            
            var leagueName = localStorage.getItem("leagueName")
            axios.post("https://calm-retreat-42630.herokuapp.com/https://nishi7409:1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU@api.challonge.com/v1/tournaments.json", {
                api_key: "1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU",
                tournament: {
                    name: `${leagueName}`,
                    description: "Dice Tracker league",
                    open_signup: false,
                    hide_forum: true,
                },
            }, {headers: {'Content-Type': 'application/json'}}).then(function(response) {
                if (response.status == 200) {
                    localStorage.setItem("challongeLeagueID", response.data.tournament.id)
                    localStorage.setItem("challongeURLForEmbed", response.data.tournament.url)
                } else {
                    console.log(response)
                }
                
            })
            
            //Successful team matching
            var bulkTeamNames = []
            for (var y = 0; y < JSON.parse(localStorage.getItem("teamLength")); y++){
                bulkTeamNames.push(this.teamMap.get(y)[0])
                axios.post("http://127.0.0.1:8000/addTeamToLeague/", {
                    name: this.teamMap.get(y)[0],
                    user1: this.teamMap.get(y)[1],
                    user2: this.teamMap.get(y)[2],
                    ownerUsername: localStorage.getItem('username'),
                }, {headers: {'Content-Type': 'application/json'}}).then(response => {
                    if (response.data.response == false){
                        Vue.notify({
                            position: "top center",
                            group: "server",
                            text: response.data.error,
                            type: "error",
                        })
                        return(undefined);
                    }else{
                        console.log(response.data.error)
                    }
                })
            }
            var participantList = []
            for (var i = 0; i < bulkTeamNames.length; i++) {
                participantList.push({"name" : bulkTeamNames[i], "misc": "optional field"})
            }
            // make call to api (Dice Tracker api) that saves data to league
            setTimeout(function() {
                axios.post(`http://127.0.0.1:8000/saveChallongeData`, {
                    leagueName: localStorage.getItem("leagueName"),
                    challongeID: localStorage.getItem("challongeLeagueID"),
                    challongeURL: localStorage.getItem("challongeURLForEmbed"),
                }, {headers: {'Content-Type': 'application/json'}}).then(function(response) {
                    if (response.status == 200) {
                        console.log("Added challonge info to league")
                    }
                })
            }, 3000)
            setTimeout(function () {
                axios.post(`https://calm-retreat-42630.herokuapp.com/https://nishi7409:1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU@api.challonge.com/v1/tournaments/${localStorage.getItem('challongeLeagueID')}/participants/bulk_add.json`, {
                    api_key: "1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU",
                    participants: participantList
                }, {headers: {'Content-Type': 'application/json'}}).then(function(response) {
                    if (response.status == 200) {
                        console.log("added team")
                    }
                })
            }, 5000)
            
            setTimeout(function () {
                axios.post(`https://calm-retreat-42630.herokuapp.com/https://nishi7409:1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU@api.challonge.com/v1/tournaments/${localStorage.getItem('challongeLeagueID')}/participants/randomize.json`, {
                    api_key: "1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU",
                }, {headers: {'Content-Type': 'application/json'}}).then(response => {
                    if (response.status == 200) {
                        console.log(response)
                    } else {
                        console.log(response)
                    }
                })
            }, 7000)
            setTimeout(function () {
                axios.post(`https://calm-retreat-42630.herokuapp.com/https://nishi7409:1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU@api.challonge.com/v1/tournaments/${localStorage.getItem('challongeLeagueID')}/start.json`, {
                    api_key: "1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU",
                }, {headers: {'Content-Type': 'application/json'}}).then(response => {
                    if (response.status == 200) {
                        console.log("STARTED FOR REAL")
                        console.log(response)
                    } else {
                        console.log("didn't start :(")
                    }
                })
            }, 9000)
            
            var matchIDs = []
            setTimeout(function () {
                axios.get(`https://calm-retreat-42630.herokuapp.com/https://nishi7409:1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU@api.challonge.com/v1/tournaments/${localStorage.getItem('challongeLeagueID')}/matches.json`, {
                params: {
                    api_key: "1WVHeSGXHOaYXWyNfysXl1NduV4tsNDmgcrfY6hU",
                    state: "all"
                }
                }).then(function (response) {
                    for (var x = 0; x < response.data.length; x++){
                        matchIDs.push(response.data[x].match.id)
                    }
                })
            }, 13000)
            localStorage.setItem("allMatchIDs4Storage", JSON.stringify(matchIDs))
            setTimeout(function() {
                axios.post(`http://127.0.0.1:8000/saveMatchIDs`, {
                    leagueName: localStorage.getItem("leagueName"),
                    matchIDs: matchIDs,
                }, {headers: {'Content-Type': 'application/json'}}).then(function(response) {
                    if (response.status == 200) {
                        console.log("Added data to league")
                    }
                })
            }, 16000)
            console.log("DONE")
            // setTimeout(function () {
            //     window.location.href = `http://localhost:8080/dashboard/league/${localStorage.getItem("leagueName")}/bracket`
            // }, 20000)
        },
        
        // Takes users from the localstorage
        extractUsers() {
            return(JSON.parse(localStorage.getItem("allUsernamesForLeague")))
        },
        // Add to the disabled list as well as map the items map 
        addDisabled(item,id, index) {
            // Check if id exists as a key in map
            // If it doesn't, add it to the map as push the item to the disabled list
            // If it does, delete the disabled item and update the map using the id as the key
            if (this.map.get(id) == null){
                this.map.set(id, item)
                this.disabledItems.push(item)
            }else if(this.map.get(id) != null){
                console.log(this.map.get(id))
                this.disabledItems.splice(this.disabledItems.indexOf(this.map.get(id)), 1)
                this.map.set(id, item)
                this.disabledItems.push(item)
            }
            // Updates the team map with the teammates
            var newList = this.teamMap.get(index)
            if (id.includes("a")){
                newList[1] = item
            }else{
                newList[2] = item
            }
            
            this.teamMap.set(index, newList)
            console.log(this.teamMap.get(index))
        }
    },
    computed: {
        // Determines what items should be disabled
        computeItems() {
            return this.items.map(item => {
                return {
                    text: item, 
                    disabled: this.disabledItems.includes(item)
                }
            })
        },
    },
    // Before page loads run this function
    beforeMount() {
        // Post request to recieve league information
        // Used for finding the length of teams as well as usernames
        axios.post("http://127.0.0.1:8000/allLeagueUsers/", {
            leagueName: localStorage.getItem("leagueName")
        }, {headers: {'Content-Type': 'application/json'}}).then(function (response) {
            if (response.data.response == false){
                console.log("help")
            }else{
                console.log(JSON.stringify(response.data.error))
                localStorage.setItem("allUsernamesForLeague", JSON.stringify(response.data.error))
                localStorage.setItem("teamLength", JSON.stringify(response.data.teamLength))
                
            }
        })
        this.teamLength = JSON.parse(localStorage.getItem("teamLength"))
        // Create the teams map
        for (var x = 0; x < JSON.parse(localStorage.getItem("teamLength")); x++){
            this.teamMap.set(x, ["Team "+x,"",""])
        }
        
    }
}
</script>