<template>
  <div>
    <v-card
      dark
      tile
      width="100%"
      style="position: sticky; top: 204px; z-index: 1300"
    >
      <v-toolbar class="pl-5 pr-5" dense extension-height="45">
        <v-spacer></v-spacer>
        <v-btn @click="template"
          >Template
          <v-icon>mdi-export</v-icon>
        </v-btn>
        <v-btn @click="ingestDialog = !ingestDialog">
          Import
          <v-icon>mdi-import</v-icon>
        </v-btn>
        <v-btn
          v-if="ingested"
          @click="
            userAuthentications = originalUserAuthentications;
            ingested = false;
          "
        >
          Revert All
          <v-icon color="red">mdi-undo</v-icon>
        </v-btn>
        <v-btn v-if="ingested" @click="saveAll">
          Save All
          <v-icon color="green">mdi-content-save</v-icon>
        </v-btn>
      </v-toolbar>
      <v-spacer class="pt-1" dark></v-spacer>
    </v-card>

    <authentication-bar
      :changed="userAuthentication.changed"
      :edit="userAuthentication.edit"
      :reminder="reminder"
      @edit="userAuthentication.edit = !userAuthentication.edit"
      :userAuthentication="userAuthentication"
      @save="saveAuthentication"
      @change="userAuthentication.changed = true"
      @revert="revert"
      @history="history"
    />
    <v-row>
      <v-col cols="4">
        <v-row justify="end">
          <v-col cols="6">
            <v-select
              v-model="groupFilter"
              :items="groups"
              label="Filter Group"
              chips
              filled
              dense
              dark
              clearable
              height="30"
              append-icon="mdi-chevron-down"
            ></v-select>
          </v-col>
          <v-col cols="6">
            <v-text-field
              label="Filter Name"
              filled
              dense
              dark
              height="30"
              v-model="userFilter"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-card
          flat
          class="transparent mt-4"
          style="overflow-y: scroll"
          height="70vh"
        >
          <v-card-title class="white--text">Users</v-card-title>

          <v-card-text>
            <v-divider class="mt-n4 mb-5" color="white"></v-divider>
            <v-card
              v-for="user of filterAuth(userAuthentications)"
              :key="user.id"
              class="ma-1 mb-4"
              @click="
                user.id === userAuthentication.id
                  ? (userAuthentication = {})
                  : (userAuthentication = getUserAuthentication(user)),
                  (authentication = {})
              "
              tile
              height="40px"
            >
              <v-img
                contain
                style="position: absolute"
                :gradient="
                  user.id !== userAuthentication.id
                    ? 'to top right, rgb(24 2 2 / 55%), rgb(56 83 219 / 40%)'
                    : ''
                "
                height="100%"
                width="100%"
              />
              <v-row justify="space-between">
                <div class="font-weight-bold mt-1 mb-1 pt-1 pb-1 ml-4">
                  {{ user.lastName }}, {{ user.firstName }}
                </div>
                <div class="mt-1 mb-1 overline">
                  {{ user.group }}
                </div>
                <v-badge
                  :color="
                    user.changed
                      ? 'blue'
                      : user.missing
                      ? 'red'
                      : user.expired
                      ? 'orange'
                      : ''
                  "
                  :icon="
                    user.changed
                      ? 'mdi-pencil'
                      : user.missing
                      ? 'mdi-exclamation'
                      : user.expired
                      ? 'mdi-clock'
                      : ''
                  "
                  offset-x="25"
                  offset-y="16"
                >
                  <div
                    class="highlight ma-1 pa-1 mr-4 rounded-0 d-inline-block"
                  >
                    {{ user.authentications.length }} services
                  </div></v-badge
                >
              </v-row>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
      <v-divider vertical color="white"></v-divider>
      <v-col>
        <v-row no-gutters justify="end">
          <v-col cols="3">
            <v-btn
              small
              @click="flagged = !flagged"
              class="mt-3"
              outlined
              dense
              dark
              :color="flagged ? 'yellow' : ''"
              >{{ flagged ? "Showing Only Flagged" : "Show Only Flagged" }}
            </v-btn>
          </v-col>
          <v-col cols="2">
            <v-text-field
              class="mr-2"
              label="Filter Service"
              filled
              dense
              dark
              v-model="serviceFilter"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-divider class="mt-3" color="white"></v-divider>





        <v-row
          no-gutters
          class="ma-10 mt-3"
          v-if="activeServices && userAuthentication.id"
        >
          <v-card
            v-for="(services, classification) in userServices"
            :key="classification"
            class="d-flex flex-wrap"
            color="transparent"
            flat
            tile
          >
            <v-card-title class="white--text">{{
              classification.toUpperCase()
            }}</v-card-title>

            <v-card-text>
              <v-divider class="mt-n4 mb-5" color="white"></v-divider>
              <v-row>
                <v-badge
                  class="ma-2"
                  :value="getIconAndColor(service.id)[2]"
                  :color="getIconAndColor(service.id)[1]"
                  bordered
                  :icon="getIconAndColor(service.id)[0]"
                  overlap
                  v-for="service in services"
                  :key="service.id"
                  offset-x="15"
                  offset-y="15"
                >

                  <v-dialog
                      v-model="dialogBox"
                      width="80vw"
                      height="90vh"
                      style="z-index: 1500"
                  >
                      <template  v-slot:activator="{ on, props }">
                        <v-card tile width="147">



                          <v-img
                              :gradient="
                        service.id !== authentication.serviceId
                          ? 'to top right, rgb(24 2 2 / 85%), rgb(56 83 219 / 70%)'
                          : ''
                      "
                              contain
                              :src="service.logo"
                              height="84"
                              width="147"
                              @click="
                        service.id === authentication.serviceId
                          ? (authentication = {})
                          : (authentication = getAuthentication(service.id))"
                              v-bind="props"
                              v-on="on"
                          />
                        </v-card>
                      </template>

                      <!--Star With a VCARD after the Initial Justify Tag-->
                      <v-card>

                        <v-card-title>

                          <!--1. Image and Current Credential Status is put in inside a V-TITLE-->
                          <v-card tile class="white" flat width="80">
                            <v-img
                                contain
                                :gradient="
                      !userAuthentication.edit
                        ? 'to top right, rgb(24 2 2 / 85%), rgb(56 83 219 / 70%)'
                        : ''
                    "
                                :src="getLogo(authentication.serviceId)"
                                height="47"
                                width="80"
                            />
                          </v-card>

                          <!--Top right section of box which tells credential dates-->
                          <v-row no-gutters>

                            <!--Each div acts like an "if" statement possible text-->

                            <!--1. Credentials are missing or have never been inputted-->
                            <div v-if="!authentication.id" class="pl-3">
                              Credentials are missing
                            </div>

                            <!--2. Credentials have expired with date-->
                            <div v-else-if="expired(authentication) > 0" class="pl-3">
                              <v-row no-gutters>
                                Credentials have Expired:
                                {{
                                  dayjs(authentication.date)
                                      .add(authentication.expirationDays, "days")
                                      .format("ddd, DD MMM YYYY")
                                }}
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Required Password Reset Period:
                                  {{ authentication.expirationDays }} days
                                </div>
                              </v-row>
                            </div>

                            <!--3. Credentials will expire soon with date-->
                            <div
                                v-else-if="expired(authentication) + expirationWarning > 0"
                                class="pl-3"
                            >
                              <v-row no-gutters>
                                Credentials will Expire on
                                {{
                                  dayjs(authentication.date)
                                      .add(authentication.expirationDays, "days")
                                      .format("ddd, DD MMM YYYY")
                                }}
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Required Reset Period:
                                  {{ authentication.expirationDays }} days
                                </div>
                              </v-row>
                            </div>

                            <!--4. Credentials SET (with date)-->
                            <div v-else class="pl-3">
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY  HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                            </div>
                          </v-row>
                        </v-card-title>

                        <!--Horizontal Line Divider-->
                        <v-divider></v-divider>





                        <!--Bottom half of the dialog box to input credentials when edited-->
                        <v-row class="ma-3" no-gutters>
                          <v-col>
                            <v-card
                                tile
                                @click="!userAuthentication.edit ? setReminder() : ''"
                            >

                              <!--Text field to input the Useranme-->
                              <v-text-field
                                  v-show="
                        userAuthentication.edit &&
                        !authentication.clearCredentials
                      "
                                  label="Username"
                                  tabindex="1"
                                  filled
                                  dense
                                  v-model="authentication.username"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                              ></v-text-field
                              ></v-card>
                          </v-col>
                        </v-row>
                        <v-row class="ma-3 mt-5" no-gutters>
                          <v-col>
                            <v-card
                                tile
                                @click="!userAuthentication.edit ? setReminder() : ''"
                            >

                              <!--Text field to input the Password-->
                              <v-text-field
                                  v-show="
                        userAuthentication.edit &&
                        !authentication.clearCredentials
                      "
                                  label="Password"
                                  tabindex="2"
                                  filled
                                  dense
                                  v-model="authentication.password"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                              ></v-text-field>
                            </v-card>
                          </v-col>
                        </v-row>

                        <!--Extra two options to force password reset change & clear creds-->
                        <v-row
                            v-if="
                                authentication.resetEnabled &&
                                !authentication.clearCredentials &&
                                userAuthentication.edit
                              "
                            class="ma-3 mt-5"
                            no-gutters
                        >
                          <v-col>
                            <v-card tile>

                              <!--1. Checkbox to force a password reset-->
                              <v-checkbox
                                  class="mb-0 pb-0"
                                  :disabled="!userAuthentication.edit || !authentication.id"
                                  dense
                                  label="Force Client Automated Password Reset at Next Login"
                                  v-model="authentication.clientPasswordReset"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                                  off-icon="mdi-checkbox-blank-outline"
                                  on-icon="mdi-checkbox-marked"
                              ></v-checkbox>
                              <div v-if="!authentication.id" class="ml-5 caption red--text">
                                Force Password Reset is Disabled because credentials are
                                missing
                              </div>
                            </v-card>
                          </v-col>
                        </v-row>
                        <v-row
                            v-show="userAuthentication.edit && authentication.id"
                            class="ma-3 mt-5"
                            no-gutters
                        >
                          <v-col>
                            <v-card tile>

                              <!--2. Checkbox to clear current credentials-->
                              <v-checkbox
                                  dense
                                  label="Clear Stored Credentials"
                                  v-model="authentication.clearCredentials"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                        authentication.clientPasswordReset = false;
                      "
                                  off-icon="mdi-checkbox-blank-outline"
                                  on-icon="mdi-checkbox-marked"
                              ></v-checkbox>
                            </v-card>
                          </v-col>
                        </v-row>



                        <!--4. Button To Close?-->
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                              color="blue-darken-1"
                              variant="text"
                              @click="dialogBox = !dialogBox"
                          >
                            Close!
                          </v-btn>
                        </v-card-actions>
                      </v-card>


                  </v-dialog>


                </v-badge>
              </v-row>
            </v-card-text>
          </v-card>
        </v-row>
        <v-divider color="white"></v-divider>
      </v-col>
    </v-row>



    <v-dialog
        v-model="ingestDialog"
        width="80vw"
        height="90vh"
        style="z-index: 1500"
    >

      <Ingest @ingest="ingest" />
    </v-dialog>
  </div>
</template>










<template>
  <div>
    <v-card
      dark
      tile
      width="100%"
      style="position: sticky; top: 204px; z-index: 1300"
    >
      <v-toolbar class="pl-5 pr-5" dense extension-height="45">
        <v-spacer></v-spacer>
        <v-btn @click="template"
          >Template
          <v-icon>mdi-export</v-icon>
        </v-btn>
        <v-btn @click="ingestDialog = !ingestDialog">
          Import
          <v-icon>mdi-import</v-icon>
        </v-btn>
        <v-btn
          v-if="ingested"
          @click="
            userAuthentications = originalUserAuthentications;
            ingested = false;
          "
        >
          Revert All
          <v-icon color="red">mdi-undo</v-icon>
        </v-btn>
        <v-btn v-if="ingested" @click="saveAll">
          Save All
          <v-icon color="green">mdi-content-save</v-icon>
        </v-btn>
      </v-toolbar>
      <v-spacer class="pt-1" dark></v-spacer>
    </v-card>

    <authentication-bar
      :changed="userAuthentication.changed"
      :edit="userAuthentication.edit"
      :reminder="reminder"
      @edit="userAuthentication.edit = !userAuthentication.edit"
      :userAuthentication="userAuthentication"
      @save="saveAuthentication"
      @change="userAuthentication.changed = true"
      @revert="revert"
      @history="history"
    />
    <v-row>
      <v-col cols="4">
        <v-row justify="end">
          <v-col cols="6">
            <v-select
              v-model="groupFilter"
              :items="groups"
              label="Filter Group"
              chips
              filled
              dense
              dark
              clearable
              height="30"
              append-icon="mdi-chevron-down"
            ></v-select>
          </v-col>
          <v-col cols="6">
            <v-text-field
              label="Filter Name"
              filled
              dense
              dark
              height="30"
              v-model="userFilter"
            ></v-text-field>
          </v-col>
        </v-row>

        <v-card
          flat
          class="transparent mt-4"
          style="overflow-y: scroll"
          height="70vh"
        >
          <v-card-title class="white--text">Users</v-card-title>

          <v-card-text>
            <v-divider class="mt-n4 mb-5" color="white"></v-divider>
            <v-card
              v-for="user of filterAuth(userAuthentications)"
              :key="user.id"
              class="ma-1 mb-4"
              @click="
                user.id === userAuthentication.id
                  ? (userAuthentication = {})
                  : (userAuthentication = getUserAuthentication(user)),
                  (authentication = {})
              "
              tile
              height="40px"
            >
              <v-img
                contain
                style="position: absolute"
                :gradient="
                  user.id !== userAuthentication.id
                    ? 'to top right, rgb(24 2 2 / 55%), rgb(56 83 219 / 40%)'
                    : ''
                "
                height="100%"
                width="100%"
              />
              <v-row justify="space-between">
                <div class="font-weight-bold mt-1 mb-1 pt-1 pb-1 ml-4">
                  {{ user.lastName }}, {{ user.firstName }}
                </div>
                <div class="mt-1 mb-1 overline">
                  {{ user.group }}
                </div>
                <v-badge
                  :color="
                    user.changed
                      ? 'blue'
                      : user.missing
                      ? 'red'
                      : user.expired
                      ? 'orange'
                      : ''
                  "
                  :icon="
                    user.changed
                      ? 'mdi-pencil'
                      : user.missing
                      ? 'mdi-exclamation'
                      : user.expired
                      ? 'mdi-clock'
                      : ''
                  "
                  offset-x="25"
                  offset-y="16"
                >
                  <div
                    class="highlight ma-1 pa-1 mr-4 rounded-0 d-inline-block"
                  >
                    {{ user.authentications.length }} services
                  </div></v-badge
                >
              </v-row>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
      <v-divider vertical color="white"></v-divider>
      <v-col>
        <v-row no-gutters justify="end">
          <v-col cols="3">
            <v-btn
              small
              @click="flagged = !flagged"
              class="mt-3"
              outlined
              dense
              dark
              :color="flagged ? 'yellow' : ''"
              >{{ flagged ? "Showing Only Flagged" : "Show Only Flagged" }}
            </v-btn>
          </v-col>
          <v-col cols="2">
            <v-text-field
              class="mr-2"
              label="Filter Service"
              filled
              dense
              dark
              v-model="serviceFilter"
            ></v-text-field>
          </v-col>
        </v-row>
        <v-divider class="mt-3" color="white"></v-divider>




        <v-row
          no-gutters
          class="ma-10 mt-3"
          v-if="activeServices && userAuthentication.id"
        >
          <v-card
            v-for="(services, classification) in userServices"
            :key="classification"
            class="d-flex flex-wrap"
            color="transparent"
            flat
            tile
          >
            <v-card-title class="white--text">{{
              classification.toUpperCase()
            }}</v-card-title>

            <v-card-text>
              <v-divider class="mt-n4 mb-5" color="white"></v-divider>
              <v-row>
                <v-badge
                  class="ma-2"
                  :value="getIconAndColor(service.id)[2]"
                  :color="getIconAndColor(service.id)[1]"
                  bordered
                  :icon="getIconAndColor(service.id)[0]"
                  overlap
                  v-for="service in services"
                  :key="service.id"
                  offset-x="15"
                  offset-y="15"
                >




                  <v-card tile width="147">
                    <v-img
                      :gradient="
                        service.id !== authentication.serviceId
                          ? 'to top right, rgb(24 2 2 / 85%), rgb(56 83 219 / 70%)'
                          : ''
                      "
                      contain
                      :src="service.logo"
                      height="84"
                      width="147"
                      @click="
                        service.id === authentication.serviceId
                          ? (authentication = {})
                          : (authentication = getAuthentication(service.id))"
                    />
                  </v-card>


                  <v-row no-gutters v-if="service.id === authentication.serviceId">

                    <v-dialog
                        v-model="dialogBox"
                        width="80vw"
                        height="90vh"
                        style="z-index: 1500"
                    >
                      <template  v-slot:activator="{ on, props }">
                        <v-btn
                            color="primary"
                            v-bind="props"
                            v-on="on"
                            class="black--text"
                            v-show="service.active"
                            style="display: block; margin: 0 auto;"

                        >
                          Edit Creds
                        </v-btn>
                      </template>

                      <!--Star With a VCARD after the Initial Justify Tag-->
                      <v-card>

                        <v-card-title>

                          <!--1. Image and Current Credential Status is put in inside a V-TITLE-->
                          <v-card tile class="white" flat width="80">
                            <v-img
                                contain
                                :gradient="
                      !userAuthentication.edit
                        ? 'to top right, rgb(24 2 2 / 85%), rgb(56 83 219 / 70%)'
                        : ''
                    "
                                :src="getLogo(authentication.serviceId)"
                                height="47"
                                width="80"
                            />
                          </v-card>

                          <!--Top right section of box which tells credential dates-->
                          <v-row no-gutters>

                            <!--Each div acts like an "if" statement possible text-->

                            <!--1. Credentials are missing or have never been inputted-->
                            <div v-if="!authentication.id" class="pl-3">
                              Credentials are missing
                            </div>

                            <!--2. Credentials have expired with date-->
                            <div v-else-if="expired(authentication) > 0" class="pl-3">
                              <v-row no-gutters>
                                Credentials have Expired:
                                {{
                                  dayjs(authentication.date)
                                      .add(authentication.expirationDays, "days")
                                      .format("ddd, DD MMM YYYY")
                                }}
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Required Password Reset Period:
                                  {{ authentication.expirationDays }} days
                                </div>
                              </v-row>
                            </div>

                            <!--3. Credentials will expire soon with date-->
                            <div
                                v-else-if="expired(authentication) + expirationWarning > 0"
                                class="pl-3"
                            >
                              <v-row no-gutters>
                                Credentials will Expire on
                                {{
                                  dayjs(authentication.date)
                                      .add(authentication.expirationDays, "days")
                                      .format("ddd, DD MMM YYYY")
                                }}
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                              <v-row no-gutters>
                                <div class="caption">
                                  Required Reset Period:
                                  {{ authentication.expirationDays }} days
                                </div>
                              </v-row>
                            </div>

                            <!--4. Credentials SET (with date)-->
                            <div v-else class="pl-3">
                              <v-row no-gutters>
                                <div class="caption">
                                  Credentials Set:
                                  {{
                                    dayjs(authentication.date).format(
                                        "ddd, DD MMM YYYY  HH:mm"
                                    )
                                  }}
                                </div>
                              </v-row>
                            </div>
                          </v-row>
                        </v-card-title>

                        <!--Horizontal Line Divider-->
                        <v-divider></v-divider>


                        <!--Bottom half of the dialog box to input credentials when edited-->
                        <v-row class="ma-3" no-gutters>
                          <v-col>
                            <v-card
                                tile
                                @click="!userAuthentication.edit ? setReminder() : ''"
                            >

                              <!--Text field to input the Useranme-->
                              <v-text-field
                                  v-show="
                        userAuthentication.edit &&
                        !authentication.clearCredentials
                      "
                                  label="Username"
                                  tabindex="1"
                                  filled
                                  dense
                                  v-model="authentication.username"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                              ></v-text-field
                              ></v-card>
                          </v-col>
                        </v-row>
                        <v-row class="ma-3 mt-5" no-gutters>
                          <v-col>
                            <v-card
                                tile
                                @click="!userAuthentication.edit ? setReminder() : ''"
                            >

                              <!--Text field to input the Password-->
                              <v-text-field
                                  v-show="
                        userAuthentication.edit &&
                        !authentication.clearCredentials
                      "
                                  label="Password"
                                  tabindex="2"
                                  filled
                                  dense
                                  v-model="authentication.password"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                              ></v-text-field>
                            </v-card>
                          </v-col>
                        </v-row>

                        <!--Extra two options to force password reset change & clear creds-->
                        <v-row
                            v-if="
                  authentication.resetEnabled &&
                  !authentication.clearCredentials &&
                  userAuthentication.edit
                "
                            class="ma-3 mt-5"
                            no-gutters
                        >
                          <v-col>
                            <v-card tile>

                              <!--1. Checkbox to force a password reset-->
                              <v-checkbox
                                  class="mb-0 pb-0"
                                  :disabled="!userAuthentication.edit || !authentication.id"
                                  dense
                                  label="Force Client Automated Password Reset at Next Login"
                                  v-model="authentication.clientPasswordReset"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                      "
                                  off-icon="mdi-checkbox-blank-outline"
                                  on-icon="mdi-checkbox-marked"
                              ></v-checkbox>
                              <div v-if="!authentication.id" class="ml-5 caption red--text">
                                Force Password Reset is Disabled because credentials are
                                missing
                              </div>
                            </v-card>
                          </v-col>
                        </v-row>
                        <v-row
                            v-show="userAuthentication.edit && authentication.id"
                            class="ma-3 mt-5"
                            no-gutters
                        >
                          <v-col>
                            <v-card tile>

                              <!--2. Checkbox to clear current credentials-->
                              <v-checkbox
                                  dense
                                  label="Clear Stored Credentials"
                                  v-model="authentication.clearCredentials"
                                  @change="
                        userAuthentication.changed = true;
                        authentication.changed = true;
                        authentication.clientPasswordReset = false;
                      "
                                  off-icon="mdi-checkbox-blank-outline"
                                  on-icon="mdi-checkbox-marked"
                              ></v-checkbox>
                            </v-card>
                          </v-col>
                        </v-row>


                        <!--4. Button To Close-->
                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                              color="blue-darken-1"
                              variant="text"
                              @click="dialogBox = !dialogBox"
                          >
                            Close
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>


                  </v-row>

                </v-badge>
              </v-row>
            </v-card-text>
          </v-card>
        </v-row>
        <v-divider color="white"></v-divider>




      </v-col>
    </v-row>


    <v-dialog
        v-model="ingestDialog"
        width="80vw"
        height="90vh"
        style="z-index: 1500"
    >

      <Ingest @ingest="ingest" />
    </v-dialog>
  </div>
</template>
















