<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { Robot } from "@/interfaces/interface";

const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);

const emit = defineEmits(["delete"]);

const props = defineProps({
  robots:  {
    type: Array as () => Array<Robot>,
    default: () => {},
  },
});

function deleteItem(itemId: string){
  emit("delete", [itemId, "robot"])
};
</script>

<template>
  <div v-if="props.robots.length">
    <CollapseDiv
      v-for="(item, idx) in props.robots"
      :key="idx"
      :id="'check' + idx.toString()"
      :idx="idx.toString()"
      :label="'Робот #' + (idx + 1).toString()"
    >
      <RowDivSlot :slotTwo="true" :print="true">
        <template v-slot:divTwo>
          <a
            href="#"
            @click="deleteItem(item['id'].toString())"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
        </template>
      </RowDivSlot>
      <RowDivSlot
        :label="'Проверка по кадровым данным<'"
        :value="item['employee']"
      />
      <RowDivSlot :label="'Проверка ИНН'" :value="item['inn']" />
      <RowDivSlot :label="'Проверка ФССП'" :value="item['debt']" />
      <RowDivSlot
        :label="'Проверка банкротства'"
        :value="item['bankruptcy']"
      />
      <RowDivSlot :label="'Проверка БКИ'" :value="item['bki']" />
      <RowDivSlot :label="'Проверка судебных дел'" :value="item['courts']" />
      <RowDivSlot
        :label="'Проверка по списку террористов'"
        :value="item['terrorist']"
      />
      <RowDivSlot
        :label="'Проверка нахождения в розыске'"
        :value="item['mvd']"
      />
      <RowDivSlot
        :label="'Дата'"
        :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
      />
    </CollapseDiv>
  </div>
</template>
