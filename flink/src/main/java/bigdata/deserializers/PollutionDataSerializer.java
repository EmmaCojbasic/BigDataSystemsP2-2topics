package bigdata.deserializers;

import bigdata.pojo.PollutionData;
import org.apache.flink.api.common.serialization.SerializationSchema;
import com.google.gson.Gson;
import org.apache.flink.api.common.typeinfo.TypeInformation;


import java.io.Serializable;
import java.nio.charset.StandardCharsets;

public class PollutionDataSerializer implements SerializationSchema<PollutionData> {

    private static final long serialVersionUID = 1L;
    private transient Gson gson;

    @Override
    public byte[] serialize(PollutionData pollutionData) {
        if (gson == null) {
            gson = new Gson();
        }
        String json = gson.toJson(pollutionData);
        return json.getBytes(StandardCharsets.UTF_8);
    }

}

