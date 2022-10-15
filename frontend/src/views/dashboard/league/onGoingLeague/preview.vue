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