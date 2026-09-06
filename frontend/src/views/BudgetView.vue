<script setup>
import BudgetSettingsCard from '../components/BudgetSettingsCard.vue'
import PageShell from '../components/PageShell.vue'
</script>

<template>
  <PageShell>
    <template #sticky>
      <h1 class="text-xl sm:text-2xl font-bold text-green-800">Ngân sách</h1>
    </template>

    <BudgetSettingsCard />
  </PageShell>
</template>
