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
        Schema::create('maintenance_records', function (Blueprint $table) {
            $table->id();
            $table->foreignId('item_id')->constrained('items')->onDelete('cascade');
            $table->date('maintenance_date');
            $table->enum('reason', ['Wet', 'Overheat', 'Wear', 'Electrical', 'Other']);
            $table->unsignedBigInteger('condition_before_id');
            $table->unsignedBigInteger('condition_after_id');
            $table->text('technician_notes')->nullable();
            $table->timestamps();
            
            $table->foreign('condition_before_id')
                ->references('id')
                ->on('conditions')
                ->onDelete('cascade');
                
            $table->foreign('condition_after_id')
                ->references('id')
                ->on('conditions')
                ->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('maintenance_records');
    }
};
