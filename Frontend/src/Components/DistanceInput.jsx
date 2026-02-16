import { useState } from "react";



function DistanceInput({ distance, setDistance }) {

              return (
                <div className="max-w-sm mx-auto mt-10">
      <div className="bg-white p-6 rounded-2xl shadow-lg border border-slate-100 transition-all hover:shadow-xl">
        <label 
          htmlFor="distance-input" 
          className="block text-sm font-semibold text-slate-700 mb-2 ml-1"
        >
          Wpisz Dystans
        </label>
        
        <div className="relative flex items-center">
          <input
            id="distance-input"
            type="number"
            value={distance}
            onChange={(e) => {
              // Pozwalamy tylko na cyfry i jedną kropkę/przecinek
              const val = e.target.value.replace(',', '.');
              if (/^\d*\.?\d*$/.test(val)) {
                setDistance(val);
              }
            }}
            placeholder="0.00"
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl 
                       text-slate-900 font-medium outline-none transition-all
                       focus:ring-2 focus:ring-blue-500 focus:border-transparent 
                       focus:bg-white placeholder:text-slate-400"
          />
          
          <div className="absolute right-4 text-slate-400 font-medium pointer-events-none">
            m
          </div>
        </div>
        
        <p className="mt-3 text-[10px] text-slate-400 uppercase tracking-wider font-bold text-center">
          Jednostka: metry (m)
        </p>
      </div>
    </div>
              );

}

export default DistanceInput;