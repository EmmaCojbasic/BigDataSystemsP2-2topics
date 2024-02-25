package bigdata.analytics;

import bigdata.deserializers.*;
import bigdata.pojo.*;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.WindowedStream;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;

import java.util.Date;

public class LaneAnalyzer {
    public static DataStream<PollutionData> laneAggregation(WindowedStream<EmissionInfo, String, TimeWindow> stream) {
        return stream
                .process(new LaneAggregator());
    }

    public static DataStream<TrafficData> calculateVehiclesOnLane(WindowedStream<VehicleInfo, String, TimeWindow> stream) {
        return stream
                .aggregate(new CountVehiclesOnLane())
                .map(new MapFunction<Tuple2<String, Integer>, TrafficData>() {
                    @Override
                    public TrafficData map(Tuple2<String, Integer> vehCounts) throws Exception {
                        return new TrafficData(new Date(), vehCounts.f0, vehCounts.f1);
                    }
                });
    }

}
