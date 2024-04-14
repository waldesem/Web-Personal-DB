<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces/interface";

const IconRelative = defineAsyncComponent(
  () => import("@components/content/elements/IconRelative.vue")
);
const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
)
const PoligrafForm = defineAsyncComponent(
  () => import("@components/content/forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(() => {
  emit("get-item", "poligraf");
});

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  poligrafs: {
    type: Array as () => Array<Pfo>,
    default: () => [],
  },
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Pfo>{},
  showActions: false,
});

function submitForm(form: Object) {
  emit(
    "submit",
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form
  );
  poligraf.value.action = "";
}
console.log(props.poligrafs);
</script>

<template>
  <div class="py-3">
    <div class="text-end">
      <IconRelative 
        v-if="poligraf.action !== 'create' && !props.printPage"
        :title="`Добавить`"
        :icon-class="`bi bi-heart-pulse fs-1`"
        @onclick="poligraf.action = 'create'"
      />
    </div>
    <PoligrafForm
      v-if="poligraf.action"
      :poligraf="poligraf.item"
      @submit="submitForm"
      @cancel="poligraf.action = ''"
    />
    <div v-else
     @mouseover="poligraf.showActions = true"
     @mouseout="poligraf.showActions = false"
    >
      <div v-if="props.poligrafs.length"> 
        <div class="mb-3" v-for="(item, idx) in props.poligrafs" :key="idx">
          <div class="card card-body">
            <LabelSlot>
              <ActionIcons v-show="poligraf.showActions"
                @delete="emit('delete', item['id'].toString(), 'poligraf')"
                @update="
                  poligraf.action = 'update';
                  poligraf.item = item;
                  poligraf.itemId = item['id'].toString();
                "
              />
            </LabelSlot>
            <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
            <LabelSlot :label="'Результат'">{{ item["results"] }}</LabelSlot>
            <LabelSlot :label="'Сотрудник'">{{ item["officer"] }}</LabelSlot>
            <LabelSlot :label="'Дата'">
              {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
            </LabelSlot>
            <FileForm 
            :accept="'*'" 
            @submit="emit('file')" 
          />
          </div>
        </div>
      </div>
      <p v-else>Данные отсутствуют</p>
    </div>
  </div>
</template>
