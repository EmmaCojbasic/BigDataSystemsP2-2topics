package bigdata.deserializers;

import bigdata.deserializers.*;
import bigdata.pojo.*;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import com.google.gson.Gson;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class EmissionInfoDeserializer implements DeserializationSchema<EmissionInfo> {          // DONE

    private static final long serialVersionUID = 1L;

    @Override
    public EmissionInfo deserialize(byte[] bytes) throws IOException {
        String json = new String(bytes, StandardCharsets.UTF_8);
        Gson gson = new Gson();
        return gson.fromJson(json, EmissionInfo.class);
    }

    @Override
    public boolean isEndOfStream(EmissionInfo emissionInfo) {
        return false;
    }

    @Override
    public TypeInformation<EmissionInfo> getProducedType() {
        return TypeInformation.of(EmissionInfo.class);
    }
}
