<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('supply_usages', function (Blueprint $table) {
            $table->id();
            $table->foreignId('item_id')->constrained('items')->onDelete('cascade');
            $table->string('period'); // e.g., "Q1 2025"
            $table->integer('usage')->default(0);
            $table->integer('stock_start')->nullable();
            $table->integer('stock_end')->nullable();
            $table->boolean('restocked')->default(false);
            $table->integer('restock_qty')->default(0);
            $table->timestamps();
            
            // Index for efficient queries by item and period
            $table->index(['item_id', 'period']);
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('supply_usages');
    }
};
