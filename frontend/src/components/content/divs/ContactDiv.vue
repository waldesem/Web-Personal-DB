<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { stateAnketa, stateUser } from "@/state";
import { Contact } from "@/interfaces";

const DropDownHead = defineAsyncComponent(
  () => import("@components/content/elements/DropDownHead.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const ContactForm = defineAsyncComponent(
  () => import("@components/content/forms/ContactForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);


const actions = ref(false);
const itemId = ref('');
const edit = ref(false);
const contact = ref(<Contact>{});

function cancelAction(){
  edit.value = false;
  itemId.value = "";
  const collapseContact = document.getElementById('contacter');
  collapseContact?.setAttribute('class', 'collapse card card-body mb-3');
};
</script>

<template>
  <DropDownHead :id="'contacter'" :header="'Контакты'"/>
  <div class="collapse card card-body mb-3" id="contacter">
    <ContactForm @cancel="cancelAction"/>
  </div>
  <div v-if="stateAnketa.anketa.contacts.length"> 
    <div 
      v-for="(item, idx) in stateAnketa.anketa.contacts" :key="idx"
      @mouseover="actions = true"
      @mouseout="actions = false" 
      class="card card-body mb-3"
    >
      <ContactForm
        v-if="edit && itemId == item['id'].toString()" 
        :contact="contact"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons 
            v-show="actions &&
              stateAnketa.anketa.persons['user_id'] == stateUser.user.userId &&
              stateAnketa.anketa.persons['standing']"
            @delete="stateAnketa.deleteItem(item['id'].toString(), 'contacts')"
            @update="
              contact = item;
              itemId = item['id'].toString()
              edit = true;
            "
            :hide="true"
          />
        </LabelSlot>
        <LabelSlot :label="'Вид'">{{ item['view'] }}</LabelSlot>
        <LabelSlot :label="'Контакт'">{{ item['contact'] }}</LabelSlot>
      </div>
    </div>
  </div>
  <p v-else>Данные отсутствуют</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>